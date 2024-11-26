import { useState, useCallback } from 'react';

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
import Checkbox from '@mui/material/Checkbox';
import ListItemText from '@mui/material/ListItemText';
import { fDate } from 'src/utils/format-time';
import { fCurrency } from 'src/utils/format-number';
import IconButton from '@mui/material/IconButton';
import { Label } from 'src/components/label';
import { Scrollbar } from 'src/components/scrollbar';
import { usePopover, CustomPopover } from 'src/components/custom-popover';
import { Iconify } from 'src/components/iconify';
import MenuList from '@mui/material/MenuList';
import MenuItem from '@mui/material/MenuItem';
import FilteredTable from './components/tableau';
import { DeclarationToolbar } from './declaration-toolbar';
import { INVOICE_STATUS_OPTIONS } from 'src/_mock';
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

export function DeclarationDetails({ invoice }, selected, onSelectRow) {
  const [currentStatus, setCurrentStatus] = useState(invoice?.status);

  const popover = usePopover();

  const handleChangeStatus = useCallback((event) => {
    setCurrentStatus(event.target.value);
  }, []);

  const renderList = (
    <Scrollbar sx={{ mt: 5 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell width={40}></TableCell>
            <TableCell sx={{ typography: 'subtitle2' }}>Numero Passeport</TableCell>
            <TableCell align="right">Nom & Prénom</TableCell>
            <TableCell align="right">Nationalité</TableCell>

            <TableCell align="right">Fonction</TableCell>
          </TableRow>
        </TableHead>
      </Table>
    </Scrollbar>
  );

  return (
    <>
      <DeclarationToolbar
        invoice={invoice}
        currentStatus={currentStatus || ''}
        onChangeStatus={handleChangeStatus}
        statusOptions={INVOICE_STATUS_OPTIONS}
      />
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

        <FilteredTable />

        <Divider sx={{ mt: 5, borderStyle: 'dashed' }} />
      </Card>
    </>
  );
}
