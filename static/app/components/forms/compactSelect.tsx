import {Fragment, useMemo, useRef, useState} from 'react';
import {useTheme} from '@emotion/react';
import styled from '@emotion/styled';
import {FocusScope} from '@react-aria/focus';
import {useListBox, useOption} from '@react-aria/listbox';
import {mergeProps, useResizeObserver} from '@react-aria/utils';
import {Item} from '@react-stately/collections';
import {ListProps, useListState} from '@react-stately/list';
import {AnimatePresence} from 'framer-motion';

import Badge from 'sentry/components/badge';
// import Button from 'sentry/components/button';
import DropdownButton, {DropdownButtonProps} from 'sentry/components/dropdownButtonV2';
// import LoadingIndicator from 'sentry/components/loadingIndicator';
import MenuListItem, {MenuListItemProps} from 'sentry/components/menuListItem';
import {Overlay, PositionWrapper} from 'sentry/components/overlay';
import {IconCheckmark} from 'sentry/icons';
import space from 'sentry/styles/space';
import {defined} from 'sentry/utils';
import useOverlay, {UseOverlayProps} from 'sentry/utils/useOverlay';

interface BaseOptionType extends MenuListItemProps {
  value: string;
}

interface BaseProps<OptionType> extends ListProps<OptionType>, UseOverlayProps {
  options: Array<OptionType & {options?: OptionType[]}>;
  /**
   * Pass class name to the outer wrap
   */
  className?: string;
  /**
   * Whether the dropdown menu should close upon selection/deselection.
   */
  closeOnSelect?: boolean;
  disabled?: boolean;
  /**
   * Whether new options are being loaded. When true, CompactSelect will
   * display a loading indicator in the header.
   */
  isLoading?: boolean;
  isSearchable?: boolean;
  multiple?: boolean;
  /**
   * Tag name for the outer wrap, defaults to `div`
   */
  renderWrapAs?: React.ElementType;
  searchPlaceholder?: string;
  /**
   * Optionally replace the trigger button with a different component. Note
   * that the replacement must have the `props` and `ref` (supplied in
   * TriggerProps) forwarded its outer wrap, otherwise the accessibility
   * features won't work correctly.
   */
  trigger?: (props: DropdownButtonProps) => React.ReactNode;
  /**
   * By default, the menu trigger will be rendered as a button, with
   * triggerLabel as the button label.
   */
  triggerLabel?: React.ReactNode;
  /**
   * If using the default button trigger (i.e. the custom `trigger` prop has
   * not been provided), then `triggerProps` will be passed on to the button
   * component.
   */
  triggerProps?: DropdownButtonProps;
}

interface SingleSelectProps<OptionType> extends BaseProps<OptionType> {
  defaultValue?: React.Key;
  multiple?: false;
  onChange?: (value: React.Key) => void;
  value?: React.Key;
}

interface MultipleSelectProps<OptionType> extends BaseProps<OptionType> {
  multiple: true;
  defaultValue?: React.Key[];
  onChange?: (values: React.Key[]) => void;
  value?: React.Key[];
}

/**
 * A <ul /> element with accessibile behaviors & attributes.
 * https://react-spectrum.adobe.com/react-aria/useListBox.html
 */
function ListBox({state, ...props}) {
  const ref = useRef<HTMLUListElement>(null);
  const {listBoxProps} = useListBox({...props}, state, ref);

  return (
    <ListBoxWrap {...listBoxProps} ref={ref}>
      {[...state.collection].map(item => (
        <Option key={item.key} item={item} state={state} />
      ))}
    </ListBoxWrap>
  );
}

/**
 * A <li /> element with accessibile behaviors & attributes.
 * https://react-spectrum.adobe.com/react-aria/useListBox.html
 */
function Option({item, state}) {
  const ref = useRef<HTMLLIElement>(null);
  const multiple = state.selectionManager.selectionMode === 'multiple';
  const {label, details, leadingItems, trailingItems, priority} = item.props;

  const {optionProps, isSelected, isFocused, isDisabled} = useOption(
    {key: item.key},
    state,
    ref
  );

  return (
    <MenuListItem
      {...optionProps}
      ref={ref}
      label={label}
      details={details}
      isFocused={isFocused}
      isDisabled={isDisabled}
      priority={priority ?? isSelected ? 'primary' : 'default'}
      leadingItems={
        <Fragment>
          <CheckWrap multiple={multiple} isSelected={isSelected}>
            {isSelected && (
              <IconCheckmark
                size={multiple ? 'xs' : 'sm'}
                color={multiple ? 'white' : undefined}
              />
            )}
          </CheckWrap>
          {leadingItems}
        </Fragment>
      }
      trailingItems={trailingItems}
    />
  );
}

/**
 * Base select component that takes options as children:
 *
 * <BaseSelectComponent>
 *   <Item ...>...</Item>
 *   <Item ...>...</Item>
 * </BaseSelectComponent>
 *
 * To provide options as an array prop, use CompactSelect.
 */
function BaseCompactSelect<OptionType extends BaseOptionType>({
  // Select props
  onChange,
  defaultValue,
  value,
  disabled,
  // isSearchable = false,
  // searchPlaceholder = 'Search…',
  multiple,
  disallowEmptySelection,
  // Trigger button & wrapper props
  trigger,
  triggerLabel: triggerLabelProp,
  triggerProps,
  className,
  closeOnSelect,
  position = 'bottom-start',
  ...props
}:
  | Omit<SingleSelectProps<OptionType>, 'options'>
  | Omit<MultipleSelectProps<OptionType>, 'options'>) {
  // Get overlay props
  const {
    state: overlayState,
    triggerRef,
    triggerProps: overlayTriggerProps,
    overlayProps,
  } = useOverlay({type: 'listbox', position});

  // Calculate the current trigger element's width. This will be used as
  // the min width for the menu.
  const [triggerWidth, setTriggerWidth] = useState<number>();
  // Update triggerWidth when its size changes using useResizeObserver
  useResizeObserver({
    ref: triggerRef,
    onResize: async () => {
      // Wait until the trigger element finishes rendering, otherwise
      // ResizeObserver might throw an infinite loop error.
      await new Promise(resolve => window.setTimeout(resolve));
      const newTriggerWidth = triggerRef.current?.offsetWidth;
      newTriggerWidth && setTriggerWidth(newTriggerWidth);
    },
  });

  /**
   * Props to be passed into useListState().
   */
  const listStateProps = useMemo<Partial<ListProps<OptionType>>>(() => {
    if (multiple) {
      return {
        selectionMode: 'multiple',
        selectedKeys: value,
        defaultSelectedKeys: defaultValue,
        disallowEmptySelection,
        onSelectionChange: sel => {
          const newValue = [...sel];
          onChange?.(newValue);

          if (closeOnSelect) {
            overlayState.close();
          }
        },
      };
    }

    return {
      selectionMode: 'single',
      selectedKeys: defined(value) ? [value] : undefined,
      defaultSelectedKeys: defined(defaultValue) ? [defaultValue] : undefined,
      disallowEmptySelection: disallowEmptySelection ?? true,
      onSelectionChange: sel => {
        const newValue = typeof sel === 'string' ? sel : sel.values().next().value;
        onChange?.(newValue);

        if (closeOnSelect !== false) {
          overlayState.close();
        }
      },
    };
  }, [
    multiple,
    closeOnSelect,
    value,
    defaultValue,
    disallowEmptySelection,
    onChange,
    overlayState,
  ]);

  /**
   * Select state, contains list of all options and selected options.
   */
  const listState = useListState({
    ...props,
    ...listStateProps,
  });

  /**
   * Trigger label, generated from current selection value. If more than one
   * option is selected, then a badge will appear with the count.
   */
  const triggerLabel: React.ReactNode = useMemo(() => {
    if (defined(triggerLabelProp)) {
      return triggerLabelProp;
    }

    const {selectedKeys} = listState.selectionManager;
    const firstSelectedOption = listState.collection.getItem(
      selectedKeys.values().next().value
    );

    return (
      <Fragment>
        <TriggerLabel>{firstSelectedOption?.textValue}</TriggerLabel>
        {selectedKeys.size > 1 && <StyledBadge text={`+${selectedKeys.size - 1}`} />}
      </Fragment>
    );
  }, [triggerLabelProp, listState.selectionManager, listState.collection]);

  const theme = useTheme();
  return (
    <MenuControlWrap className={className}>
      {trigger ? (
        trigger(
          mergeProps(triggerProps, overlayTriggerProps, {
            isOpen: overlayState.isOpen,
            disabled,
          })
        )
      ) : (
        <DropdownButton
          isOpen={overlayState.isOpen}
          disabled={disabled}
          {...mergeProps(triggerProps, overlayTriggerProps)}
        >
          {triggerLabel}
        </DropdownButton>
      )}
      <AnimatePresence>
        {overlayState.isOpen && (
          <FocusScope autoFocus contain restoreFocus>
            <PositionWrapper zIndex={theme.zIndex.tooltip} {...overlayProps}>
              <StyledOverlay minWidth={triggerWidth}>
                <ListBox state={listState} shouldFocusOnHover />
              </StyledOverlay>
            </PositionWrapper>
          </FocusScope>
        )}
      </AnimatePresence>
    </MenuControlWrap>
  );
}

/**
 * A select component with a button trigger instead of an input trigger.
 */
function CompactSelect<OptionType extends BaseOptionType>({
  options,
  disabled: disabledProp,
  ...props
}: SingleSelectProps<OptionType> | MultipleSelectProps<OptionType>) {
  const disabled = disabledProp || options?.length === 0;

  return (
    <BaseCompactSelect {...props} disabled={disabled}>
      {options.map(opt => (
        <Item key={opt.value} {...opt}>
          {opt.label}
        </Item>
      ))}
    </BaseCompactSelect>
  );
}

export default CompactSelect;

const MenuControlWrap = styled('div')``;

const TriggerLabel = styled('span')`
  ${p => p.theme.overflowEllipsis}
  text-align: left;
`;

const StyledBadge = styled(Badge)`
  flex-shrink: 0;
  top: auto;
`;

// const MenuHeader = styled('div')`
//   position: relative;
//   display: flex;
//   align-items: center;
//   justify-content: space-between;
//   padding: ${space(0.25)} ${space(1)} ${space(0.25)} ${space(1.5)};
//   box-shadow: 0 1px 0 ${p => p.theme.translucentInnerBorder};
//   z-index: 1;
// `;

// const MenuTitle = styled('span')`
//   font-weight: 600;
//   font-size: ${p => p.theme.fontSizeSmall};
//   color: ${p => p.theme.headingColor};
//   white-space: nowrap;
//   margin-right: ${space(2)};
// `;

// const StyledLoadingIndicator = styled(LoadingIndicator)`
//   && {
//     margin: ${space(0.5)} ${space(0.5)} ${space(0.5)} ${space(1)};
//     height: ${space(1.5)};
//     width: ${space(1.5)};
//   }
// `;

// const ClearButton = styled(Button)`
//   font-size: ${p => p.theme.fontSizeSmall};
//   color: ${p => p.theme.subText};
// `;

const StyledOverlay = styled(Overlay)<{minWidth?: number}>`
  ${p => p.minWidth && `min-width:${p.minWidth}px;`}
`;

const ListBoxWrap = styled('ul')`
  padding: ${space(0.5)} 0;
  :focus-visible {
    outline: none;
  }
`;

const CheckWrap = styled('div')<{isSelected: boolean; multiple: boolean}>`
  display: flex;
  justify-content: center;
  align-items: center;

  ${p =>
    p.multiple
      ? `
      width: 1em;
      height: 1em;
      padding: 1px;
      border: solid 1px ${p.theme.border};
      background: ${p.theme.backgroundElevated};
      border-radius: 2px;
      box-shadow: inset ${p.theme.dropShadowLight};
      ${
        p.isSelected &&
        `
        background: ${p.theme.purple300};
        border-color: ${p.theme.purple300};
       `
      }
    `
      : `
      width: 1em;
      height: 1.4em;
      padding-bottom: 1px;
    `}
`;
