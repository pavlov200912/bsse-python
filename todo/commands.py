from todo.custom_exceptions import UserExitException
from todo.models import BaseItem
from todo.reflection import find_classes


class BaseCommand(object):
    label: str

    def perform(self, store):
        raise NotImplementedError()


class ListCommand(BaseCommand):
    label = 'list'

    def perform(self, store):
        if len(store.items) == 0:
            print('There are no items in the storage.')
            return

        for index, obj in enumerate(store.items):
            try:
                obj_repr = obj.ready_repr()
            except AttributeError:
                obj_repr = str(obj)
            print('{0}: {1}'.format(index, obj_repr))


class NewCommand(BaseCommand):
    label = 'new'

    def perform(self, store):
        classes = self._load_item_classes()

        print('Select item type:')
        for index, name in enumerate(classes.keys()):
            print('{0}: {1}'.format(index, name))

        selection = None
        selected_key = None

        while True:
            try:
                selected_key = self._select_item(classes)
            except ValueError:
                print('Bad input, try again.')
            except IndexError:
                print('Wrong index, try again.')
            else:
                break

        selected_class = classes[selected_key]
        print('Selected: {0}'.format(selected_class.__name__))
        print()

        new_object = selected_class.construct()

        store.items.append(new_object)
        print('Added {0}'.format(str(new_object)))
        return new_object

    def _load_item_classes(self) -> dict:
        # Dynamic load:
        return dict(find_classes(BaseItem))

    def _select_item(self, classes):
        selection = int(input('Input number: '))
        if selection < 0:
            raise IndexError('Index needs to be >0')
        return list(classes.keys())[selection]


class BaseDoneCommand(object):
    label = 'base_done'

    def perform(self, _store, command_tag):
        if len(_store.items) == 0:
            print('No items to do.')
            return
        print('Select item (or type exit):')
        for index, obj in enumerate(_store.items):
            try:
                obj_repr = obj.ready_repr()
            except AttributeError:
                obj_repr = str(obj)
            print('{0}: {1}'.format(index, obj_repr))

        while True:
            try:
                selected_todo_index = self._select_item(_store)
            except ValueError:
                print('Bad input, try again.')
            except IndexError as e:
                print('Wrong index. {0}. Try again.'.format(e.__repr__()))
            else:
                break

        if selected_todo_index is None:
            print()
            return

        _store.items[selected_todo_index].done = command_tag
        print('Done: {0}'.format(str(_store.items[selected_todo_index])))

    def _select_item(self, _store):
        user_input = input('Input number: ')
        if user_input == 'exit':
            return None
        selection = int(user_input)
        if selection < 0:
            raise IndexError('Index needs to be >=0')
        if selection >= len(_store.items):
            raise IndexError('Index needs to be <{0}'.format(len(_store.items)))
        return selection


class DoneCommand(BaseCommand, BaseDoneCommand):
    label = 'done'

    def perform(self, _store):
        BaseDoneCommand.perform(self, _store, True)


class UndoneCommand(BaseCommand, BaseDoneCommand):
    label = 'undone'

    def perform(self, _store):
        BaseDoneCommand.perform(self, _store, False)


class ExitCommand(BaseCommand):
    label = 'exit'

    def perform(self, _store):
        raise UserExitException('See you next time!')
