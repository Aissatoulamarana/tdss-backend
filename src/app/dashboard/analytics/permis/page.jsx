import { CONFIG } from 'src/config-global';

import { PermisAnalyticsView} from 'src/sections/overview/analytics/permis/view';

// ----------------------------------------------------------------------

export const metadata = { title: `Dashboard - ${CONFIG.appName}` };

export default function Page() {
  return <PermisAnalyticsView />;
}
