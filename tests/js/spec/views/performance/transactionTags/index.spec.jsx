import {browserHistory} from 'react-router';

import {initializeOrg} from 'sentry-test/initializeOrg';
import {act, mountWithTheme, screen, waitFor} from 'sentry-test/reactTestingLibrary';

import ProjectsStore from 'sentry/stores/projectsStore';
import {OrganizationContext} from 'sentry/views/organizationContext';
import TransactionTags from 'sentry/views/performance/transactionSummary/transactionTags';

const TEST_RELEASE_NAME = 'test-project@1.0.0';

function initializeData({query} = {query: {}}) {
  const features = ['discover-basic', 'performance-view'];
  const organization = TestStubs.Organization({
    features,
    projects: [TestStubs.Project()],
  });
  const initialData = initializeOrg({
    organization,
    router: {
      location: {
        query: {
          transaction: 'Test Transaction',
          project: '1',
          ...query,
        },
      },
    },
  });
  act(() => ProjectsStore.loadInitialData(initialData.organization.projects));
  return initialData;
}

const WrappedComponent = ({organization, ...props}) => {
  return (
    <OrganizationContext.Provider value={organization}>
      <TransactionTags organization={organization} {...props} />
    </OrganizationContext.Provider>
  );
};

describe('Performance > Transaction Tags', function () {
  let histogramMock;

  beforeEach(function () {
    browserHistory.replace = jest.fn();
    MockApiClient.addMockResponse({
      url: '/organizations/org-slug/projects/',
      body: [],
    });
    MockApiClient.addMockResponse({
      url: '/organizations/org-slug/tags/',
      body: [],
    });
    MockApiClient.addMockResponse({
      url: '/organizations/org-slug/tags/user.email/values/',
      body: [],
    });
    MockApiClient.addMockResponse({
      url: '/organizations/org-slug/events-facets-performance/',
      body: {
        meta: {
          tags_key: 'string',
          tags_value: 'string',
          sumdelta: 'duration',
          count: 'integer',
          frequency: 'number',
          comparison: 'number',
          aggregate: 'number',
        },
        data: [
          {
            tags_key: 'hardwareConcurrency',
            tags_value: '4',
            sumdelta: 45773.0,
            count: 83,
            frequency: 0.05,
            comparison: 1.45,
            aggregate: 2000.5,
          },
          {
            tags_key: 'effectiveConnectionType',
            tags_value: '4g',
            sumdelta: 45773.0,
            count: 83,
            frequency: 0.05,
            comparison: 1.45,
            aggregate: 2000.5,
          },
          {
            tags_key: 'release',
            tags_value: TEST_RELEASE_NAME,
            sumdelta: 45773.0,
            count: 83,
            frequency: 0.05,
            comparison: 1.45,
            aggregate: 2000.5,
          },
        ],
      },
    });
    histogramMock = MockApiClient.addMockResponse({
      url: '/organizations/org-slug/events-facets-performance-histogram/',
      body: {
        meta: {
          count: 'integer',
          histogram_measurements_lcp_120_360_1: 'number',
          tags_key: 'string',
          tags_value: 'string',
        },
        data: [
          {
            histogram_measurements_lcp_120_360_1: 600,
            tags_value: '4',
            tags_key: 'hardwareConcurrency',
            count: 3,
          },
        ],
      },
    });
    MockApiClient.addMockResponse({
      url: '/organizations/org-slug/events-has-measurements/',
      body: {measurements: false},
    });
    MockApiClient.addMockResponse({
      url: '/organizations/org-slug/sdk-updates/',
      body: [],
    });
    MockApiClient.addMockResponse({
      url: '/prompts-activity/',
      body: {},
    });
  });

  afterEach(function () {
    histogramMock.mockReset();
    MockApiClient.clearMockResponses();
    act(() => ProjectsStore.reset());
  });

  it('renders basic UI elements', async function () {
    const initialData = initializeData();
    mountWithTheme(
      <WrappedComponent
        organization={initialData.organization}
        location={initialData.router.location}
      />,
      {context: initialData.routerContext}
    );

    // It shows the sidebar
    expect(await screen.findByTestId('tags-page-content')).toBeInTheDocument();

    // It shows the header
    expect(await screen.findByTestId('transaction-header')).toBeInTheDocument();

    expect(browserHistory.replace).toHaveBeenCalledWith({
      query: {
        project: '1',
        statsPeriod: '14d',
        tagKey: 'hardwareConcurrency',
        transaction: 'Test Transaction',
      },
    });

    // It shows a table
    expect(await screen.findByTestId('grid-editable')).toBeInTheDocument();
  });

  it('Default tagKey is set when loading the page without one', async function () {
    const initialData = initializeData();
    mountWithTheme(
      <WrappedComponent
        organization={initialData.organization}
        location={initialData.router.location}
      />,
      {context: initialData.routerContext}
    );

    // Table is loaded.
    // The tagKey change will cause a full page re-render, so wait for the component to mount
    await waitFor(async () =>
      expect(await screen.findByTestId('grid-editable')).toBeInTheDocument()
    );

    expect(browserHistory.replace).toHaveBeenCalledWith({
      query: {
        project: '1',
        statsPeriod: '14d',
        tagKey: 'hardwareConcurrency',
        transaction: 'Test Transaction',
      },
    });

    expect(histogramMock).toHaveBeenCalledTimes(1);
    expect(histogramMock).toHaveBeenNthCalledWith(
      1,
      expect.anything(),
      expect.objectContaining({
        query: expect.objectContaining({
          statsPeriod: '14d',
          tagKey: 'hardwareConcurrency',
        }),
      })
    );
  });

  it('Passed tagKey gets used when calling queries', async function () {
    const initialData = initializeData({query: {tagKey: 'effectiveConnectionType'}});

    mountWithTheme(
      <WrappedComponent
        organization={initialData.organization}
        location={initialData.router.location}
      />,
      {context: initialData.routerContext}
    );

    // Table is loaded.
    await waitFor(async () =>
      expect(await screen.findByTestId('grid-editable')).toBeInTheDocument()
    );

    expect(browserHistory.replace).toHaveBeenCalledWith({
      query: {
        project: '1',
        statsPeriod: '14d',
        tagKey: 'effectiveConnectionType',
        transaction: 'Test Transaction',
      },
    });

    expect(histogramMock).toHaveBeenCalledTimes(1);
    expect(histogramMock).toHaveBeenNthCalledWith(
      1,
      expect.anything(),
      expect.objectContaining({
        query: expect.objectContaining({
          statsPeriod: '14d',
          tagKey: 'effectiveConnectionType',
        }),
      })
    );
  });

  it('creates links to releases if the release tag is selected', async () => {
    const initialData = initializeData({query: {tagKey: 'release'}});

    mountWithTheme(
      <WrappedComponent
        organization={initialData.organization}
        location={initialData.router.location}
      />,
      {context: initialData.routerContext}
    );

    // Table is loaded.
    await waitFor(async () =>
      expect(await screen.findByTestId('grid-editable')).toBeInTheDocument()
    );

    // Release link is properly setup
    expect(screen.getByText(TEST_RELEASE_NAME)).toBeInTheDocument();
    expect(screen.getByText(TEST_RELEASE_NAME).parentElement).toHaveAttribute(
      'href',
      `/organizations/${initialData.organization.slug}/releases/${encodeURIComponent(
        TEST_RELEASE_NAME
      )}?project=${initialData.router.location.query.project}`
    );
  });
});