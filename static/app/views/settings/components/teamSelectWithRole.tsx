import React from 'react';
import styled from '@emotion/styled';
import debounce from 'lodash/debounce';

import Button from 'sentry/components/button';
import DropdownAutoComplete from 'sentry/components/dropdownAutoComplete';
import {Item} from 'sentry/components/dropdownAutoComplete/types';
import DropdownButton from 'sentry/components/dropdownButton';
import {TeamBadge} from 'sentry/components/idBadge/teamBadge';
import Link from 'sentry/components/links/link';
import LoadingIndicator from 'sentry/components/loadingIndicator';
import {Panel, PanelBody, PanelHeader, PanelItem} from 'sentry/components/panels';
import RoleSelectControl from 'sentry/components/roleSelectControl';
import {DEFAULT_DEBOUNCE_DURATION} from 'sentry/constants';
import {IconSubtract} from 'sentry/icons';
import {t} from 'sentry/locale';
import space from 'sentry/styles/space';
import {Member, OrgRole, Team, TeamRole} from 'sentry/types';
import useOrganization from 'sentry/utils/useOrganization';
import useTeams from 'sentry/utils/useTeams';
import EmptyMessage from 'sentry/views/settings/components/emptyMessage';
import {
  hasOrgRoleOverwrite,
  RoleOverwritePanelAlert,
} from 'sentry/views/settings/organizationTeams/roleOverwriteWarning';

type Props = {
  member: Member;

  /**
   * callback when teams are added
   */
  onAddTeam: (teamSlug: string) => void;
  /**
   * Callback when roles are modified for the member
   */
  onChangeRole: (teamSlug: string, role: string) => void;

  /**
   * Callback when teams are removed
   */
  onRemoveTeam: (teamSlug: string) => void;

  orgRole: Member['orgRole'];

  teamRoles: Member['teamRoles'];

  /**
   * Should button be disabled
   */
  disabled?: boolean;

  /**
   * Used to determine whether we should show a loading state while waiting for teams
   */
  loadingTeams?: boolean;
};

function TeamSelect({
  member,
  orgRole,
  teamRoles,
  onAddTeam,
  onChangeRole,
  onRemoveTeam,
  disabled,
  loadingTeams,
}: Props) {
  const {teams, onSearch, fetching} = useTeams();
  const {orgRoleList, teamRoleList} = member;

  const handleAddTeam = (option: Item) => {
    const team = teams.find(tm => tm.slug === option.value);
    if (team) {
      onAddTeam(team.slug);
    }
  };

  const renderBody = () => {
    if (Object.keys(teamRoles).length === 0) {
      return <EmptyMessage>{t('No Teams assigned')}</EmptyMessage>;
    }

    const rows = [...teamRoles].sort((a, b) => (a.teamSlug > b.teamSlug ? 1 : -1));

    return (
      <React.Fragment>
        <RoleOverwritePanelAlert
          orgRole={orgRole}
          orgRoleList={orgRoleList}
          teamRoleList={teamRoleList}
        />
        {rows.map(teamMembership => {
          const {teamSlug, role} = teamMembership;
          const team = teams.find(tm => tm.slug === teamMembership.teamSlug);
          if (!team) {
            return <div key={teamSlug}>Error finding data for #{teamSlug}</div>;
          }

          return (
            <TeamRow
              disabled={disabled}
              key={teamSlug}
              team={team}
              teamRole={role}
              orgRole={orgRole}
              onRemove={slug => onRemoveTeam(slug)}
              onChangeRole={onChangeRole}
            />
          );
        })}
      </React.Fragment>
    );
  };

  // Only show options that aren't selected in the dropdown
  const teamRoleslugs = teamRoles.map(r => r.teamSlug);
  const remainingTeams = teams.filter(tm => !teamRoleslugs.includes(tm.slug));
  const options = remainingTeams.map((team, index) => ({
    index,
    value: team.slug,
    searchKey: team.slug,
    label: <DropdownTeamBadge avatarSize={18} team={team} />,
  }));

  return (
    <Panel>
      <PanelHeader hasButtons>
        {t('Team')}
        <DropdownAutoComplete
          items={options}
          busyItemsStillVisible={fetching}
          onChange={debounce<(e: React.ChangeEvent<HTMLInputElement>) => void>(
            e => onSearch(e.target.value),
            DEFAULT_DEBOUNCE_DURATION
          )}
          onSelect={handleAddTeam}
          emptyMessage={t('No teams')}
          // menuHeader={menuHeader}
          disabled={disabled}
          alignMenu="right"
        >
          {({isOpen}) => (
            <DropdownButton
              aria-label={t('Add Team')}
              isOpen={isOpen}
              size="xsmall"
              disabled={disabled}
            >
              {t('Add Team')}
            </DropdownButton>
          )}
        </DropdownAutoComplete>
      </PanelHeader>

      <PanelBody>{loadingTeams ? <LoadingIndicator /> : renderBody()}</PanelBody>
    </Panel>
  );
}

type TeamRowProps = {
  onChangeRole: Props['onChangeRole'];
  onRemove: Props['onRemoveTeam'];
  orgRole: OrgRole['id'];
  team: Team;
  teamRole: TeamRole['id'] | null;
  disabled?: boolean;
};

const TeamRow = ({
  onChangeRole,
  onRemove,
  orgRole,
  team,
  teamRole,
  disabled,
}: TeamRowProps) => {
  const organization = useOrganization();
  const {teamRoleList, orgRoleList} = organization;
  const isRoleOverwritten = hasOrgRoleOverwrite({orgRole, orgRoleList, teamRoleList});

  const teamRoleObj = isRoleOverwritten
    ? teamRoleList[1]
    : teamRoleList.find(r => r.id === teamRole) || teamRoleList[0];

  return (
    <TeamRolesPanelItem>
      <div>
        <Link to={`/settings/${organization.slug}/teams/${team.slug}/`}>
          <TeamBadge team={team} />
        </Link>
      </div>

      <div>
        {organization.features.includes('team-roles') && (
          <RoleSelectControl
            disabled={isRoleOverwritten}
            disableUnallowed={false}
            roles={teamRoleList}
            value={teamRoleObj?.id}
            onChange={option => onChangeRole(team.slug, option.value)}
          />
        )}
      </div>

      <div>
        <Button
          size="xsmall"
          icon={<IconSubtract isCircled size="xs" />}
          disabled={disabled}
          onClick={() => onRemove(team.slug)}
        >
          {t('Remove')}
        </Button>
      </div>
    </TeamRolesPanelItem>
  );
};

const DropdownTeamBadge = styled(TeamBadge)`
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};
  text-transform: none;
`;

export const TeamRolesPanelItem = styled(PanelItem)`
  display: grid;
  grid-template-columns: minmax(120px, 4fr) minmax(120px, 2fr) minmax(100px, 1fr);
  gap: ${space(2)};
  align-items: center;

  > div:last-child {
    margin-left: auto;
  }
`;

export default TeamSelect;
