import { paths } from 'src/routes/paths';

import { CONFIG } from 'src/config-global';

import { SvgColor } from 'src/components/svg-color';

// ----------------------------------------------------------------------

const icon = (name) => <SvgColor src={`${CONFIG.assetsDir}/assets/icons/navbar/${name}.svg`} />;

const ICONS = {
  job: icon('ic-job'),
  blog: icon('ic-blog'),
  chat: icon('ic-chat'),
  mail: icon('ic-mail'),
  user: icon('ic-user'),
  file: icon('ic-file'),
  lock: icon('ic-lock'),
  tour: icon('ic-tour'),
  order: icon('ic-order'),
  label: icon('ic-label'),
  blank: icon('ic-blank'),
  kanban: icon('ic-kanban'),
  folder: icon('ic-folder'),
  penalite: icon('ic-course'),
  facture: icon('ic-banking'),
  booking: icon('ic-booking'),
  paiement: icon('ic-invoice'),
  product: icon('ic-product'),
  calendar: icon('ic-calendar'),
  disabled: icon('ic-disabled'),
  external: icon('ic-external'),
  menuItem: icon('ic-menu-item'),
  declaration: icon('ic-ecommerce'),
  analytics: icon('ic-analytics'),
  dashboard: icon('ic-dashboard'),
  parameter: icon('ic-parameter'),
};

// ----------------------------------------------------------------------

export const navData = [
  /**
   * Overview
   */
  {
    subheader: "Vue d'ensemble",
    items: [
      { title: 'Dashboard', path: paths.dashboard.root, icon: ICONS.dashboard },
      {
        title: 'Statistiques',
        path: paths.dashboard.analytics.root,
        icon: ICONS.analytics,
        children: [
          { title: 'Declaration', path: paths.dashboard.analytics.declaration },
          { title: 'Facture', path: paths.dashboard.analytics.facture },
          { title: 'Paiement', path: paths.dashboard.analytics.paiement },
          { title: 'Penalité', path: paths.dashboard.group.root },
          { title: 'Permis de travail', path: paths.dashboard.analytics.permis },
        ],
      },
      {
        title: 'Déclarations',
        path: paths.dashboard.declaration.list,
        icon: ICONS.declaration,
      },
      {
        title: 'Factures',
        path: paths.dashboard.factures.list,
        icon: ICONS.facture,
      },
      {
        title: 'Paiements',
        path: paths.dashboard.paiements.list,
        icon: ICONS.paiement,
      },

      { title: 'Penalités', path: paths.dashboard.penalite.list, icon: ICONS.penalite },
    ],
  },
  /**
   * Management
   */
  {
    subheader: 'Administration',
    items: [
      {
        title: 'Utilisateurs',
        path: paths.dashboard.user.root,
        icon: ICONS.user,
        children: [
          { title: 'Listes Utilisateurs ', path: paths.dashboard.user.list },
          { title: 'Nouveau', path: paths.dashboard.user.new },
        ],
      },
      {
        title: 'Fonction',
        path: paths.dashboard.fonction.root,
        icon: ICONS.job,
        children: [
          { title: 'Listes Fonctions', path: paths.dashboard.fonction.list },
          { title: 'Nouvelle', path: paths.dashboard.group.five },
        ],
      },
      {
        title: 'Client',
        path: paths.dashboard.group.root,
        icon: ICONS.tour,
        children: [
          { title: 'Listes  ', path: paths.dashboard.group.root },
          { title: 'Ajouter', path: paths.dashboard.group.five },
        ],
      },
    ],
  },
];
