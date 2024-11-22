import { CONFIG } from 'src/config-global';

import { JobListView } from 'src/sections/administration/fonction/view';

// ----------------------------------------------------------------------

export const metadata = { title: `Job list | Dashboard - ${CONFIG.appName}` };

export default function Page() {
  return <JobListView />;
}
