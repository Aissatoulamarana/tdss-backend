import { CONFIG } from 'src/config-global';

import { PenaliteListView } from 'src/sections/overview/penalite/view';

// ----------------------------------------------------------------------

export const metadata = { title: `Penalités | Dashboard - ${CONFIG.appName}` };

export default function Page() {
  return <PenaliteListView />;
}
