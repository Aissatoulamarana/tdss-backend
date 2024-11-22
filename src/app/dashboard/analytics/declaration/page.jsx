import { CONFIG } from 'src/config-global';

import { OverviewAnalyticsView } from 'src/sections/overview/analytics/declaration/view';

// ----------------------------------------------------------------------

export const metadata = { title: `Dashboard - ${CONFIG.appName}` };

export default function Page() {
  return <OverviewAnalyticsView />;
}
