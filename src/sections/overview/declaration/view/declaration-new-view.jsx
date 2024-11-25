'use client';

import { paths } from 'src/routes/paths';

import { DashboardContent } from 'src/layouts/dashboard';

import { CustomBreadcrumbs } from 'src/components/custom-breadcrumbs';

import { DeclarationNew } from '../declaration-new';
import { ImportFilesButton } from '../components/button-import-excel';

// ----------------------------------------------------------------------

export function DeclarationNewView() {
  return (
    <DashboardContent maxWidth="xl">
      <CustomBreadcrumbs
        heading="Nouvelle Déclarations"
        links={[
          { name: 'Tableau de bord', href: paths.dashboard.root },
          { name: 'Déclarations', href: paths.dashboard.declaration.list },
          { name: 'Nouvelle Déclaration' },
        ]}
        sx={{ mb: { xs: 3, md: 2 } }} // Marges pour les breadcrumbs
      />
      <div style={{ marginBottom: '20px' }}>
        <ImportFilesButton />
      </div>
      {/* Ajout d'espace sous ImportFilesButton */}
      <DeclarationNew />
    </DashboardContent>
  );
}
