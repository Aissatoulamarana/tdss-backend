import { useState } from 'react';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Table from '@mui/material/Table';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import { styled } from '@mui/material/styles';
import TableRow from '@mui/material/TableRow';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import Typography from '@mui/material/Typography';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';

import { fDate } from 'src/utils/format-time';
import { fCurrency } from 'src/utils/format-number';

import { Label } from 'src/components/label';
import { Scrollbar } from 'src/components/scrollbar';

// ----------------------------------------------------------------------

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  [`& .${tableCellClasses.root}`]: {
    textAlign: 'right',
    borderBottom: 'none',
    paddingTop: theme.spacing(1),
    paddingBottom: theme.spacing(1),
  },
}));

// ----------------------------------------------------------------------

export function DeclarationDetails({ invoice }) {
  const [currentStatus, setCurrentStatus] = useState(invoice?.status);

  /* const handleChangeStatus = useCallback((event) => {
    setCurrentStatus(event.target.value);
  },[]); */

  const renderList = (
    <Scrollbar sx={{ mt: 5 }}>
      <Table sx={{ minWidth: 960 }}>
        <TableHead>
          <TableRow>
            <TableCell width={40}></TableCell>
            <TableCell sx={{ typography: 'subtitle2' }}>Numero Passeport</TableCell>

            <TableCell align="right">Nom & Prénom</TableCell>
            <TableCell align="right">Fonction</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {invoice?.items.map((row, index) => (
            <TableRow key={index}>
              <TableCell>{index + 1}</TableCell>

              <TableCell>
                <Box sx={{ maxWidth: 560 }}>
                  <Typography variant="subtitle2">{row.id}</Typography>
                </Box>
              </TableCell>

              <TableCell align="right">{fCurrency(row.price * row.quantity)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Scrollbar>
  );

  return (
    <Card sx={{ pt: 5, px: 5 }}>
      <Box
        rowGap={5}
        display="grid"
        alignItems="center"
        gridTemplateColumns={{ xs: 'repeat(1, 1fr)', sm: 'repeat(2, 1fr)' }}
      >
        <Box
          component="img"
          alt="logo"
          src="/logo/logo-single.svg"
          sx={{ width: 48, height: 48 }}
        />

        <Stack spacing={1} alignItems={{ xs: 'flex-start', md: 'flex-end' }}>
          <Label
            variant="soft"
            color={
              (currentStatus === 'paid' && 'success') ||
              (currentStatus === 'pending' && 'warning') ||
              (currentStatus === 'overdue' && 'error') ||
              'default'
            }
          >
            {currentStatus}
          </Label>

          <Typography variant="h6">{invoice?.invoiceNumber}</Typography>
        </Stack>

        <Stack sx={{ typography: 'body2' }}>
          <Typography variant="subtitle2" sx={{ mb: 1 }}>
            Client
            <br />
            {invoice?.invoiceFrom.name}
          </Typography>
        </Stack>

        <Stack sx={{ typography: 'body2' }}>
          <Typography variant="subtitle2" sx={{ mb: 1 }}>
            Date de creation
          </Typography>
          {fDate(invoice?.createDate)}
        </Stack>
      </Box>
      <Divider sx={{ mt: 5, borderStyle: 'dashed' }} mb={4} />
      <Stack
        direction="row"
        justifyContent="center"
        alignItems="center"
        mb={4}
        spacing={12} // Ajoute de l'espace entre les éléments
        sx={{ typography: 'body2' }}
      >
        <Stack alignItems="center">
          <Typography variant="subtitle2" sx={{ mb: 1 }}>
            Cadres
          </Typography>
          2
        </Stack>

        <Stack alignItems="center">
          <Typography variant="subtitle2" sx={{ mb: 1 }}>
            Agents
          </Typography>
          1
        </Stack>

        <Stack alignItems="center">
          <Typography variant="subtitle2" sx={{ mb: 1 }}>
            Ouvriers
          </Typography>
          1
        </Stack>
      </Stack>

      {renderList}

      <Divider sx={{ mt: 5, borderStyle: 'dashed' }} />
    </Card>
  );
}
