import { CONFIG } from 'src/config-global';

import { UserListView } from 'src/sections/administration/user/view';

// ----------------------------------------------------------------------

export const metadata = { title: `User list | Dashboard - ${CONFIG.appName}` };

export default function Page() {
  return <UserListView />;
}
