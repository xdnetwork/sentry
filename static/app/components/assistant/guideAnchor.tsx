import {Fragment} from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import {Query} from 'history';

import {
  closeGuide,
  dismissGuide,
  nextStep,
  recordFinish,
  registerAnchor,
  unregisterAnchor,
} from 'sentry/actionCreators/guides';
import {Guide} from 'sentry/components/assistant/types';
import Button from 'sentry/components/button';
import {Body as HovercardBody, Hovercard} from 'sentry/components/hovercard';
import {t, tct} from 'sentry/locale';
import GuideStore, {GuideStoreState} from 'sentry/stores/guideStore';
import space from 'sentry/styles/space';
import theme from 'sentry/utils/theme';

type Props = {
  /** Hovercard renders the container */
  containerClassName?: string;
  offset?: string;
  onFinish?: () => void;
  // Shouldn't target be mandatory?
  position?: React.ComponentProps<typeof Hovercard>['position'];
  target?: string;
  to?: {
    pathname: string;
    query: Query;
  };
};

type State = {
  active: boolean;
  orgId: string | null;
  step: number;
  currentGuide?: Guide;
};

/**
 * A GuideAnchor puts an informative hovercard around an element.
 * Guide anchors register with the GuideStore, which uses registrations
 * from one or more anchors on the page to determine which guides can
 * be shown on the page.
 */
function GuideAnchor({children}) {
  return <Fragment>{children}</Fragment>;
}

export {GuideAnchor};

/**
 * Wraps the GuideAnchor so we don't have to render it if it's disabled
 * Using a class so we automatically have children as a typed prop
 */
type WrapperProps = {disabled?: boolean} & Props;

export default class GuideAnchorWrapper extends React.Component<WrapperProps> {
  render() {
    const {disabled, children, ...rest} = this.props;
    if (disabled || window.localStorage.getItem('hide_anchors') === '1') {
      return children || null;
    }
    return <GuideAnchor {...rest}>{children}</GuideAnchor>;
  }
}

const GuideContainer = styled('div')`
  display: grid;
  grid-template-rows: repeat(2, auto);
  gap: ${space(2)};
  text-align: center;
  line-height: 1.5;
  background-color: ${p => p.theme.purple300};
  border-color: ${p => p.theme.purple300};
  color: ${p => p.theme.white};
`;

const GuideContent = styled('div')`
  display: grid;
  grid-template-rows: repeat(2, auto);
  gap: ${space(1)};

  a {
    color: ${p => p.theme.white};
    text-decoration: underline;
  }
`;

const GuideTitle = styled('div')`
  font-weight: bold;
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;

const GuideDescription = styled('div')`
  font-size: ${p => p.theme.fontSizeMedium};
`;

const GuideAction = styled('div')`
  display: grid;
  grid-template-rows: repeat(2, auto);
  gap: ${space(1)};
`;

const StyledButton = styled(Button)`
  font-size: ${p => p.theme.fontSizeMedium};
  min-width: 40%;
`;

const DismissButton = styled(StyledButton)`
  margin-left: ${space(1)};

  &:hover,
  &:focus,
  &:active {
    color: ${p => p.theme.white};
  }
  color: ${p => p.theme.white};
`;

const StepCount = styled('div')`
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: bold;
  text-transform: uppercase;
`;

const StyledHovercard = styled(Hovercard)`
  ${HovercardBody} {
    background-color: ${theme.purple300};
    margin: -1px;
    border-radius: ${theme.borderRadius};
    width: 300px;
  }
`;
