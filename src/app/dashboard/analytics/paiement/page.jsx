import { CONFIG } from 'src/config-global';

import { AnalyticPaiementView } from 'src/sections/overview/analytics/paiement/view';

// ----------------------------------------------------------------------

export const metadata = { title: `Dashboard - ${CONFIG.appName}` };

export default function Page() {
  return <AnalyticPaiementView />;
}
