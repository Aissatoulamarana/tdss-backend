import { CONFIG } from 'src/config-global';

import { OverviewAppView } from 'src/sections/app/view';

// ----------------------------------------------------------------------

export const metadata = { title: `Dashboard - ${CONFIG.appName}` };

export default function Page() {
  return <OverviewAppView />;
}
