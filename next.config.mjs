const isStaticExport = 'false';

const nextConfig = {
  trailingSlash: true,
  env: {
    BUILD_STATIC_EXPORT: isStaticExport,
  },
  modularizeImports: {
    '@mui/icons-material': {
      transform: '@mui/icons-material/{{member}}',
    },
    '@mui/material': {
      transform: '@mui/material/{{member}}',
    },
    '@mui/lab': {
      transform: '@mui/lab/{{member}}',
    },
  },

  // Fonction rewrites à placer à l'intérieur de nextConfig
  async rewrites() {
    return [
      {
        source: '/:path*',
        destination: 'http://localhost:8000/:path*', // L'adresse de ton serveur Django
      },
    ];
  },

  webpack(config) {
    config.module.rules.push({
      test: /\.svg$/,
      use: ['@svgr/webpack'],
    });

    return config;
  },

  ...(isStaticExport === 'true' && {
    output: 'export',
  }),
};

export default nextConfig;
