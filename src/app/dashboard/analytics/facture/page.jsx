import { CONFIG } from 'src/config-global';

import { AnalyticsFactureView } from 'src/sections/overview/analytics/factures/view';

// ----------------------------------------------------------------------

export const metadata = { title: `Dashboard - ${CONFIG.appName}` };

export default function Page() {
  return <AnalyticsFactureView />;
}
