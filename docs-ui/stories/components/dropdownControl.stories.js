import DropdownControl, {DropdownItem} from 'sentry/components/dropdownControl';
import MenuItem from 'sentry/components/menuItem';
import DropdownMenuControlV2 from 'sentry/components/dropdownMenuControlV2';

export default {
  title: 'Components/Buttons/Dropdowns/Dropdown Control',
};

export const BasicLabelKnobs = ({
  menuWidth,
  alwaysRenderMenu,
  alignRight,
  blendWithActor,
}) => {
  const menuItems = [
    {
      key: 'sectiona',
      label: 'Section A',
      children: [
        {
          key: 'item_1',
          label: 'Item 1',
        },
        {
          key: 'item_2',
          label: 'Item 2',
        },
      ],
    },
    {
      key: 'sectionb',
      label: 'Section B',
      children: [
        {
          key: 'item_3',
          label: 'Priority: Primary',
          priority: 'primary',
        },
        {
          key: 'item_4',
          label: 'Priority: Danger',
          priority: 'danger',
        },
        {
          key: 'item_5',
          label: 'Disabled',
        },
      ],
    },
  ];

  return (
    <div className="clearfix">
      <DropdownMenuControlV2
        items={menuItems}
        triggerProps={{
          prefix: 'Prefix',
        }}
        triggerLabel="Label"
        disabledKeys={['item_5']}
      />
    </div>
  );
};

BasicLabelKnobs.storyName = 'Basic Label + Knobs';
BasicLabelKnobs.args = {
  menuWidth: '',
  alwaysRenderMenu: true,
  alignRight: false,
  blendWithActor: false,
};
BasicLabelKnobs.parameters = {
  docs: {
    description: {
      story: 'Using a string value for the button label',
    },
  },
};

export const BasicMenuItem = () => (
  <div className="clearfix">
    <DropdownControl label={<em>Slanty</em>}>
      <MenuItem href="">Item</MenuItem>
      <MenuItem href="">Item</MenuItem>
    </DropdownControl>
  </div>
);

BasicMenuItem.storyName = 'Basic Menu Item';
BasicMenuItem.parameters = {
  docs: {
    description: {
      story: 'Element labels replace the button contents',
    },
  },
};

export const ElementLabel = () => (
  <div className="clearfix">
    <DropdownControl label="Created Date">
      <MenuItem href="">Item</MenuItem>
      <MenuItem href="">Item</MenuItem>
    </DropdownControl>
  </div>
);

ElementLabel.storyName = 'Element Label';
ElementLabel.parameters = {
  docs: {
    description: {
      story: 'Element labels replace the button contents',
    },
  },
};

export const PrefixedLabel = () => (
  <div className="clearfix">
    <DropdownControl buttonProps={{prefix: 'Sort By'}} label="Created Date">
      <MenuItem href="">Item</MenuItem>
      <MenuItem href="">Item</MenuItem>
    </DropdownControl>
  </div>
);

PrefixedLabel.storyName = 'Prefixed Label';
PrefixedLabel.parameters = {
  docs: {
    description: {
      story: 'Element labels replace the button contents',
    },
  },
};

export const CustomButton = () => (
  <div className="clearfix">
    <DropdownControl
      button={({getActorProps}) => <button {...getActorProps()}>click me</button>}
    >
      <MenuItem href="">Item</MenuItem>
      <MenuItem href="">Item</MenuItem>
    </DropdownControl>
  </div>
);

CustomButton.storyName = 'Custom Button';
CustomButton.parameters = {
  docs: {
    description: {
      story: 'button prop lets you replace the entire button.',
    },
  },
};
