'use client';

import { paths } from 'src/routes/paths';

import { DashboardContent } from 'src/layouts/dashboard';

import { CustomBreadcrumbs } from 'src/components/custom-breadcrumbs';

import { DeclarationEditForm } from '../declaration-edit-form';

// ----------------------------------------------------------------------

export function DeclarationEditView({ invoice }) {
  return (
    <DashboardContent>
      <CustomBreadcrumbs
        heading="Modifier"
        links={[
          { name: 'Dashboard', href: paths.dashboard.root },
          { name: 'Déclarations', href: paths.dashboard.declaration.root },
          { name: invoice?.invoiceNumber },
        ]}
        sx={{ mb: { xs: 3, md: 5 } }}
      />

      <DeclarationEditForm currentInvoice={invoice} />
    </DashboardContent>
  );
}
