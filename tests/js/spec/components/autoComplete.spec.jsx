import {useEffect} from 'react';

import {mountWithTheme} from 'sentry-test/enzyme';

import AutoComplete from 'sentry/components/autoComplete';

const items = [
  {
    name: 'Apple',
  },
  {
    name: 'Pineapple',
  },
  {
    name: 'Orange',
  },
];

/**
 * For every render, we push all injected params into `autoCompleteState`, we probably want to
 * assert against those instead of the wrapper's state since component state will be different if we have
 * "controlled" props where <AutoComplete> does not handle state
 */
describe('AutoComplete', function () {
  let wrapper;
  let input;
  let autoCompleteState = [];
  const mocks = {
    onSelect: jest.fn(),
    onClose: jest.fn(),
    onOpen: jest.fn(),
  };

  const List = ({registerItemCount, itemCount, ...props}) => {
    useEffect(() => void registerItemCount(itemCount), [itemCount, registerItemCount]);
    return <ul {...props} />;
  };

  const Item = ({registerVisibleItem, item, index, ...props}) => {
    useEffect(() => registerVisibleItem(index, item), [registerVisibleItem, index, item]);
    return <li {...props} />;
  };

  const createWrapper = props => {
    autoCompleteState = [];
    Object.keys(mocks).forEach(key => mocks[key].mockReset());

    wrapper = mountWithTheme(
      <AutoComplete {...mocks} itemToString={item => item.name} {...props}>
        {injectedProps => {
          const {
            getRootProps,
            getInputProps,
            getMenuProps,
            getItemProps,
            inputValue,
            isOpen,
            registerItemCount,
            registerVisibleItem,
          } = injectedProps;

          // This is purely for testing
          autoCompleteState.push(injectedProps);

          const filteredItems = items.filter(item =>
            item.name.toLowerCase().includes(inputValue.toLowerCase())
          );

          return (
            <div {...getRootProps()}>
              <input {...getInputProps()} />

              {isOpen && (
                <div {...getMenuProps()}>
                  <List
                    registerItemCount={registerItemCount}
                    itemCount={filteredItems.length}
                  >
                    {filteredItems.map((item, index) => (
                      <Item
                        key={item.name}
                        registerVisibleItem={registerVisibleItem}
                        index={index}
                        item={item}
                        {...getItemProps({item, index})}
                      >
                        {item.name}
                      </Item>
                    ))}
                  </List>
                </div>
              )}
            </div>
          );
        }}
      </AutoComplete>
    );

    input = wrapper.find('input');
    return wrapper;
  };

  describe('Uncontrolled', function () {
    beforeEach(() => {
      wrapper = createWrapper();
    });

    it('shows dropdown menu when input has focus', function () {
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.find('li')).toHaveLength(3);
    });

    it('only tries to close once if input is blurred and click outside occurs', async function () {
      jest.useFakeTimers();
      input.simulate('focus');
      input.simulate('blur');
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.find('li')).toHaveLength(3);
      wrapper.find('DropdownMenu').prop('onClickOutside')();
      jest.runAllTimers();
      await Promise.resolve();
      wrapper.update();

      expect(mocks.onClose).toHaveBeenCalledTimes(1);
    });

    it('only calls onClose dropdown menu when input is blurred', function () {
      jest.useFakeTimers();
      input.simulate('focus');
      input.simulate('blur');
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.find('li')).toHaveLength(3);
      jest.runAllTimers();
      wrapper.update();

      expect(wrapper.state('isOpen')).toBe(false);
      expect(wrapper.find('li')).toHaveLength(0);
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
    });

    it('handles component being unmounted and then blurred', function () {
      input.simulate('focus');
      input.simulate('blur');
      expect(wrapper.state('isOpen')).toBe(true);
      wrapper.unmount();

      // This is a bit contrived but we inputs that fetch data async
      // and then update state and the autocomplete has been removed
      // from the DOM as the collapsible section of the page has
      // been closed.
      input.simulate('keyDown', {key: 'Escape'});
      wrapper.update();
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
    });

    it('can close dropdown menu when Escape is pressed', function () {
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);

      input.simulate('keyDown', {key: 'Escape'});
      expect(wrapper.state('isOpen')).toBe(false);
    });

    it('can open and close dropdown menu using injected actions', function () {
      const [injectedProps] = autoCompleteState;
      injectedProps.actions.open();
      expect(wrapper.state('isOpen')).toBe(true);
      expect(mocks.onOpen).toHaveBeenCalledTimes(1);

      injectedProps.actions.close();
      expect(wrapper.state('isOpen')).toBe(false);
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
    });

    it('reopens dropdown menu after Escape is pressed and input is changed', function () {
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);

      input.simulate('keyDown', {key: 'Escape'});
      expect(wrapper.state('isOpen')).toBe(false);

      input.simulate('change', {target: {value: 'a'}});
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.instance().items.size).toBe(3);
    });

    it('reopens dropdown menu after item is selected and then input is changed', function () {
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);

      input.simulate('change', {target: {value: 'eapp'}});
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.instance().items.size).toBe(1);
      input.simulate('keyDown', {key: 'Enter'});
      expect(wrapper.state('isOpen')).toBe(false);

      input.simulate('change', {target: {value: 'app'}});
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.instance().items.size).toBe(2);
    });

    it('selects dropdown item by clicking and sets input to selected value', function () {
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.instance().items.size).toBe(3);

      wrapper.find('li').at(1).simulate('click');
      expect(mocks.onSelect).toHaveBeenCalledWith(
        items[1],
        expect.objectContaining({inputValue: '', highlightedIndex: 0}),
        expect.anything()
      );

      expect(wrapper.state('inputValue')).toBe('Pineapple');
      expect(wrapper.instance().items.size).toBe(0);
    });

    it('can navigate dropdown items with keyboard and select with "Enter" keypress', function () {
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.state('highlightedIndex')).toBe(0);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(1);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(2);

      expect(wrapper.instance().items.size).toBe(3);
      input.simulate('keyDown', {key: 'Enter'});

      expect(mocks.onSelect).toHaveBeenCalledWith(
        items[2],
        expect.objectContaining({inputValue: '', highlightedIndex: 2}),
        expect.anything()
      );
      expect(wrapper.instance().items.size).toBe(0);
      expect(wrapper.state('inputValue')).toBe('Orange');
    });

    it('respects list bounds when navigating filtered items with arrow keys', function () {
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.state('highlightedIndex')).toBe(0);

      input.simulate('keyDown', {key: 'ArrowUp'});
      expect(wrapper.state('highlightedIndex')).toBe(0);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(1);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(2);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(2);

      input.simulate('keyDown', {key: 'ArrowUp'});
      expect(wrapper.state('highlightedIndex')).toBe(1);

      input.simulate('keyDown', {key: 'ArrowUp'});
      expect(wrapper.state('highlightedIndex')).toBe(0);

      input.simulate('keyDown', {key: 'ArrowUp'});
      expect(wrapper.state('highlightedIndex')).toBe(0);

      expect(wrapper.instance().items.size).toBe(3);
    });

    it('can filter items and then navigate with keyboard', function () {
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.state('highlightedIndex')).toBe(0);
      expect(wrapper.instance().items.size).toBe(3);

      input.simulate('change', {target: {value: 'a'}});
      expect(wrapper.state('highlightedIndex')).toBe(0);
      expect(wrapper.state('inputValue')).toBe('a');
      // Apple, pineapple, orange
      expect(wrapper.instance().items.size).toBe(3);

      input.simulate('change', {target: {value: 'ap'}});
      expect(wrapper.state('highlightedIndex')).toBe(0);
      expect(wrapper.state('inputValue')).toBe('ap');
      expect(autoCompleteState[autoCompleteState.length - 1].inputValue).toBe('ap');
      // Apple, pineapple
      expect(wrapper.instance().items.size).toBe(2);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(1);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(1);
      expect(wrapper.instance().items.size).toBe(2);

      input.simulate('keyDown', {key: 'Enter'});
      expect(mocks.onSelect).toHaveBeenCalledWith(
        items[1],
        expect.objectContaining({inputValue: 'ap', highlightedIndex: 1}),
        expect.anything()
      );
      expect(wrapper.instance().items.size).toBe(0);
      expect(wrapper.state('inputValue')).toBe('Pineapple');
    });

    it('can reset input when menu closes', function () {
      jest.useFakeTimers();
      wrapper.setProps({resetInputOnClose: true});
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);

      input.simulate('change', {target: {value: 'a'}});
      expect(wrapper.state('inputValue')).toBe('a');

      input.simulate('blur');
      jest.runAllTimers();
      expect(wrapper.state('isOpen')).toBe(false);
      expect(wrapper.state('inputValue')).toBe('');
    });
  });

  describe('isOpen controlled', function () {
    beforeEach(function () {
      wrapper = createWrapper({isOpen: true});
    });

    it('has dropdown menu initially open', function () {
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.find('li')).toHaveLength(3);
    });

    it('closes when props change', function () {
      wrapper.setProps({isOpen: false});
      expect(wrapper.state('isOpen')).toBe(true);
      wrapper.update();

      // Menu should be closed
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.find('li')).toHaveLength(0);
    });

    it('remains closed when input is focused, but calls `onOpen`', function () {
      wrapper = createWrapper({isOpen: false});
      jest.useFakeTimers();

      expect(wrapper.state('isOpen')).toBe(false);

      input.simulate('focus');
      jest.runAllTimers();
      wrapper.update();
      expect(wrapper.state('isOpen')).toBe(false);
      expect(wrapper.find('li')).toHaveLength(0);

      expect(mocks.onOpen).toHaveBeenCalledTimes(1);
    });

    it('remains open when input focus/blur events occur, but calls `onClose`', function () {
      jest.useFakeTimers();
      input.simulate('focus');
      input.simulate('blur');
      jest.runAllTimers();
      wrapper.update();
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.find('li')).toHaveLength(3);

      // This still gets called even though menu is open
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
    });

    it('calls onClose when Escape is pressed', function () {
      expect(wrapper.state('isOpen')).toBe(true);

      input.simulate('keyDown', {key: 'Escape'});
      expect(wrapper.state('isOpen')).toBe(true);
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
    });

    it('does not open and close dropdown menu using injected actions', function () {
      const [injectedProps] = autoCompleteState;
      injectedProps.actions.open();
      expect(wrapper.state('isOpen')).toBe(true);
      expect(mocks.onOpen).toHaveBeenCalledTimes(1);

      injectedProps.actions.close();
      expect(wrapper.state('isOpen')).toBe(true);
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
    });

    it('onClose is called after item is selected', function () {
      expect(wrapper.state('isOpen')).toBe(true);

      input.simulate('change', {target: {value: 'eapp'}});
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.instance().items.size).toBe(1);
      input.simulate('keyDown', {key: 'Enter'});
      expect(wrapper.state('isOpen')).toBe(true);
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
    });

    it('selects dropdown item by clicking and sets input to selected value', function () {
      expect(wrapper.instance().items.size).toBe(3);

      wrapper.find('li').at(1).simulate('click');
      expect(mocks.onSelect).toHaveBeenCalledWith(
        items[1],
        expect.objectContaining({inputValue: '', highlightedIndex: 0}),
        expect.anything()
      );

      expect(wrapper.state('inputValue')).toBe('Pineapple');
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
    });

    it('can navigate dropdown items with keyboard and select with "Enter" keypress', function () {
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.state('highlightedIndex')).toBe(0);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(1);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(2);

      expect(wrapper.instance().items.size).toBe(3);
      input.simulate('keyDown', {key: 'Enter'});

      expect(mocks.onSelect).toHaveBeenCalledWith(
        items[2],
        expect.objectContaining({inputValue: '', highlightedIndex: 2}),
        expect.anything()
      );
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
      expect(wrapper.state('inputValue')).toBe('Orange');
    });

    it('respects list bounds when navigating filtered items with arrow keys', function () {
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.state('highlightedIndex')).toBe(0);

      input.simulate('keyDown', {key: 'ArrowUp'});
      expect(wrapper.state('highlightedIndex')).toBe(0);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(1);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(2);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(2);

      input.simulate('keyDown', {key: 'ArrowUp'});
      expect(wrapper.state('highlightedIndex')).toBe(1);

      input.simulate('keyDown', {key: 'ArrowUp'});
      expect(wrapper.state('highlightedIndex')).toBe(0);

      input.simulate('keyDown', {key: 'ArrowUp'});
      expect(wrapper.state('highlightedIndex')).toBe(0);

      expect(wrapper.instance().items.size).toBe(3);
    });

    it('can filter items and then navigate with keyboard', function () {
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.state('highlightedIndex')).toBe(0);
      expect(wrapper.instance().items.size).toBe(3);

      input.simulate('change', {target: {value: 'a'}});
      expect(wrapper.state('highlightedIndex')).toBe(0);
      expect(wrapper.state('inputValue')).toBe('a');
      // Apple, pineapple, orange
      expect(wrapper.instance().items.size).toBe(3);

      input.simulate('change', {target: {value: 'ap'}});
      expect(wrapper.state('highlightedIndex')).toBe(0);
      expect(wrapper.state('inputValue')).toBe('ap');
      expect(autoCompleteState[autoCompleteState.length - 1].inputValue).toBe('ap');
      // Apple, pineapple
      expect(wrapper.instance().items.size).toBe(2);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(1);

      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(1);
      expect(wrapper.instance().items.size).toBe(2);

      input.simulate('keyDown', {key: 'Enter'});
      expect(mocks.onSelect).toHaveBeenCalledWith(
        items[1],
        expect.objectContaining({inputValue: 'ap', highlightedIndex: 1}),
        expect.anything()
      );
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
      expect(wrapper.state('inputValue')).toBe('Pineapple');
    });

    it('can reset input value when menu closes', function () {
      jest.useFakeTimers();
      wrapper.setProps({resetInputOnClose: true});
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);

      input.simulate('change', {target: {value: 'a'}});
      expect(wrapper.state('inputValue')).toBe('a');

      input.simulate('blur');
      jest.runAllTimers();
      expect(wrapper.state('inputValue')).toBe('');
    });
  });

  describe('inputValue controlled', () => {
    beforeEach(function () {
      wrapper = createWrapper({inputValue: 'initial value'});
    });

    it('follows the inputValue prop', () => {
      expect(input.instance().value).toBe('initial value');

      wrapper.setProps({inputValue: 'new value'});

      expect(input.instance().value).toBe('new value');
    });

    it('calls onInputValueChange on input', () => {
      const onInputValueChange = jest.fn();
      wrapper.setProps({onInputValueChange});
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);

      input.simulate('change', {target: {value: 'a'}});

      expect(onInputValueChange).toHaveBeenCalledWith('a');
    });

    it('input value does not change when typed into', () => {
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);

      input.simulate('change', {target: {value: 'a'}});
      expect(wrapper.state('inputValue')).toBe('initial value');
    });

    it('input value does not change when blurred', () => {
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);

      input.simulate('blur');
      expect(input.instance().value).toBe('initial value');
    });

    it('can search for and select an item without changing the input value', () => {
      input.simulate('focus');
      wrapper.setProps({inputValue: 'apple'});
      expect(wrapper.state('isOpen')).toBe(true);

      expect(wrapper.instance().items.size).toBe(2);

      wrapper.find('li').at(1).simulate('click');

      expect(wrapper.state('isOpen')).toBe(false);
      expect(input.instance().value).toBe('apple');
    });

    it('can filter and navigate dropdown items with keyboard and select with "Enter" keypress without changing input value', function () {
      wrapper.setProps({inputValue: 'apple'});
      input.simulate('focus');
      expect(wrapper.state('isOpen')).toBe(true);
      expect(wrapper.state('highlightedIndex')).toBe(0);
      expect(wrapper.instance().items.size).toBe(2);

      input.simulate('keyDown', {key: 'ArrowDown'});
      input.simulate('keyDown', {key: 'ArrowDown'});
      input.simulate('keyDown', {key: 'ArrowDown'});
      expect(wrapper.state('highlightedIndex')).toBe(1);

      input.simulate('keyDown', {key: 'Enter'});

      expect(mocks.onSelect).toHaveBeenCalledWith(
        items[1],
        expect.objectContaining({highlightedIndex: 1}),
        expect.anything()
      );
      expect(mocks.onClose).toHaveBeenCalledTimes(1);
      expect(input.instance().value).toBe('apple');
    });
  });

  it('selects using enter key', function () {
    wrapper = createWrapper({isOpen: true, shouldSelectWithEnter: false});
    input.simulate('change', {target: {value: 'pine'}});
    input.simulate('keyDown', {key: 'Enter'});
    expect(mocks.onSelect).not.toHaveBeenCalled();

    wrapper = createWrapper({isOpen: true, shouldSelectWithEnter: true});
    input.simulate('change', {target: {value: 'pine'}});
    input.simulate('keyDown', {key: 'Enter'});
    expect(mocks.onSelect).toHaveBeenCalledWith(
      items[1],
      expect.objectContaining({inputValue: 'pine', highlightedIndex: 0}),
      expect.anything()
    );
    expect(mocks.onClose).toHaveBeenCalledTimes(1);
    expect(wrapper.state('inputValue')).toBe('Pineapple');
  });

  it('selects using tab key', function () {
    wrapper = createWrapper({isOpen: true, shouldSelectWithTab: false});
    input.simulate('change', {target: {value: 'pine'}});
    input.simulate('keyDown', {key: 'Tab'});
    expect(mocks.onSelect).not.toHaveBeenCalled();

    wrapper = createWrapper({isOpen: true, shouldSelectWithTab: true});
    input.simulate('change', {target: {value: 'pine'}});
    input.simulate('keyDown', {key: 'Tab'});
    expect(mocks.onSelect).toHaveBeenCalledWith(
      items[1],
      expect.objectContaining({inputValue: 'pine', highlightedIndex: 0}),
      expect.anything()
    );
    expect(mocks.onClose).toHaveBeenCalledTimes(1);
    expect(wrapper.state('inputValue')).toBe('Pineapple');
  });

  it('does not reset highlight state if `closeOnSelect` is false and we select a new item', function () {
    wrapper = createWrapper({closeOnSelect: false});
    jest.useFakeTimers();
    input.simulate('focus');
    expect(wrapper.state('isOpen')).toBe(true);

    input.simulate('keyDown', {key: 'ArrowDown'});
    expect(wrapper.state('highlightedIndex')).toBe(1);

    // Select item
    input.simulate('keyDown', {key: 'Enter'});

    // Should still remain open with same highlightedIndex
    expect(wrapper.state('highlightedIndex')).toBe(1);
    expect(wrapper.state('isOpen')).toBe(true);

    input.simulate('keyDown', {key: 'ArrowDown'});
    expect(wrapper.state('highlightedIndex')).toBe(2);

    // Select item
    input.simulate('keyDown', {key: 'Enter'});

    // Should still remain open with same highlightedIndex
    expect(wrapper.state('highlightedIndex')).toBe(2);
    expect(wrapper.state('isOpen')).toBe(true);
  });
});
