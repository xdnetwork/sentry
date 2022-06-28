import {initializeOrg} from 'sentry-test/initializeOrg';
import {render, screen, userEvent, waitFor} from 'sentry-test/reactTestingLibrary';

import {TeamCreate} from 'sentry/views/teamCreate';

describe('TeamCreate', function () {
  afterEach(function () {
    MockApiClient.clearMockResponses();
  });

  it('renders correctly', function () {
    const {organization, routerContext} = initializeOrg();
    const wrapper = render(
      <TeamCreate
        organization={organization}
        params={{
          orgId: organization.slug,
        }}
      />,
      {context: routerContext}
    );
    expect(wrapper.container).toSnapshot();
  });

  it('redirects to team settings on submit', async function () {
    const {organization, routerContext, router} = initializeOrg();
    const createTeamMock = MockApiClient.addMockResponse({
      url: `/organizations/${organization.slug}/teams/`,
      method: 'POST',
      body: {slug: 'new-team'},
    });
    render(
      <TeamCreate
        organization={organization}
        params={{
          orgId: organization.slug,
        }}
        router={router}
      />,
      {context: routerContext}
    );
    userEvent.type(
      screen.getByPlaceholderText('e.g. operations, web-frontend, desktop'),
      'new-team'
    );
    userEvent.click(screen.getByText('Create Team'));
    expect(createTeamMock).toHaveBeenCalledWith(
      '/organizations/org-slug/teams/',
      expect.objectContaining({
        data: {slug: 'new-team'},
      })
    );
    await waitFor(() =>
      expect(router.push).toHaveBeenCalledWith('/settings/org-slug/teams/new-team/')
    );
  });
});
