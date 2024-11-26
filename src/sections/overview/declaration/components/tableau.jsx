import React, { useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Checkbox,
  Paper,
  Toolbar,
  Typography,
  Button,
  Stack,
  Box,
  TableFooter,
  TablePagination,
  FormControlLabel,
  Switch,
} from '@mui/material';
import Tooltip from '@mui/material/Tooltip';
import { Iconify } from 'src/components/iconify';
import IconButton from '@mui/material/IconButton';

const initialRows = [
  {
    id: 1,
    number: '123456',
    name: 'Diallo Lamarana',
    nationalite: 'Guinéen',
    fonction: 'Cadres',
    permis: 'Permis A',
  },
  {
    id: 2,
    number: '123456',
    name: 'Sadou Sow ',
    nationalite: 'Senegalais',
    fonction: 'Cadres',
    permis: 'Permis B',
  },
  {
    id: 3,
    number: '123456',
    name: 'Djeinabou Diallo',
    nationalite: 'Guinéen',
    fonction: 'Agent',
    permis: 'Permis C',
  },
  {
    id: 4,
    number: '123456',
    name: 'Zoumanigui Condé',
    nationalite: 'Guinéen',
    fonction: 'Agent',
    permis: 'Permis A',
  },
  {
    id: 5,
    number: '123456',
    name: 'fassinet jule',
    nationalite: 'Corean',
    fonction: 'Cadres',
    permis: 'Permis B',
  },
  {
    id: 6,
    number: '123456',
    name: 'Camara Abdoul',
    nationalite: 'Algerien',
    fonction: 'Ouvrier',
    permis: 'Permis C',
  },
];

const documentTypes = [
  { label: 'Tous', value: 'All' },
  { label: 'Cadres', value: 'Cadres' },
  { label: 'Agent', value: 'Agent' },
  { label: 'Ouvrier', value: 'Ouvrier' },
];

const FilteredTable = () => {
  const [selected, setSelected] = useState([]);
  const [filter, setFilter] = useState('All');
  const [dense, setDense] = useState(false);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const rows =
    filter === 'All' ? initialRows : initialRows.filter((row) => row.fonction === filter);

  const isSelected = (id) => selected.includes(id);

  const handleSelectAllClick = (event) => {
    if (event.target.checked) {
      const newSelected = rows.map((row) => row.id);
      setSelected(newSelected);
    } else {
      setSelected([]);
    }
  };

  const handleRowClick = (id) => {
    setSelected((prevSelected) =>
      prevSelected.includes(id) ? prevSelected.filter((item) => item !== id) : [...prevSelected, id]
    );
  };
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };
  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <Paper>
      {/* Barre de menu pour les filtres */}

      {/* Barre d'outils conditionnelle */}
      <Toolbar
        sx={{
          pl: 2,
          pr: 2,
          display: 'flex',
          justifyContent: 'space-between',
          backgroundColor: selected.length > 0 ? 'rgba(0, 0, 255, 0.1)' : 'inherit',
        }}
      >
        {selected.length > 0 ? (
          <Typography variant="subtitle1" color="primary">
            {selected.length} sélectionné(s)
          </Typography>
        ) : (
          <Typography variant="h6"></Typography>
        )}

        {selected.length > 0 && (
          <Stack direction="row" spacing={2}>
            <Tooltip title="Deplacer">
              <IconButton color="primary">
                <Iconify icon="iconamoon:send-fill" />
              </IconButton>
            </Tooltip>
            <Tooltip title="Supprimer">
              <IconButton color="primary" onClick={confirm.onTrue}>
                <Iconify icon="solar:trash-bin-trash-bold" />
              </IconButton>
            </Tooltip>
          </Stack>
        )}
      </Toolbar>

      {/* Tableau */}
      <TableContainer>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-around',
            backgroundColor: 'rgba(0, 0, 255, 0.1)',
            padding: 1,
          }}
        >
          {documentTypes.map((fonction) => (
            <Button
              key={fonction.value}
              variant={filter === fonction.value ? 'contained' : 'text'}
              size="small"
              justify-content="flex-start"
              onClick={() => setFilter(fonction.value)}
            >
              {fonction.label} (
              {fonction.value === 'All'
                ? initialRows.length
                : initialRows.filter((row) => row.fonction === fonction.value).length}
              )
            </Button>
          ))}
        </Box>
        <Table size={dense ? 'small' : 'medium'}>
          <TableHead>
            <TableRow>
              <TableCell padding="checkbox">
                <Checkbox
                  indeterminate={selected.length > 0 && selected.length < rows.length}
                  checked={rows.length > 0 && selected.length === rows.length}
                  onChange={handleSelectAllClick}
                />
              </TableCell>
              <TableCell>Numero du passeport</TableCell>
              <TableCell>Nom & Prenom</TableCell>
              <TableCell>Nationalité</TableCell>
              <TableCell>Fonction</TableCell>
              <TableCell>Permis</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => (
              <TableRow
                key={row.id}
                hover
                role="checkbox"
                selected={isSelected(row.id)}
                onClick={() => handleRowClick(row.id)}
                style={{ cursor: 'pointer' }}
              >
                <TableCell padding="checkbox">
                  <Checkbox color="primary" checked={isSelected(row.id)} />
                </TableCell>
                <TableCell>{row.number}</TableCell>
                <TableCell>{row.name}</TableCell>
                <TableCell>{row.nationalite}</TableCell>
                <TableCell>{row.fonction}</TableCell>
                <TableCell>{row.permis}</TableCell>
              </TableRow>
            ))}
          </TableBody>
          <TableFooter>
            <TableRow>
              <TablePagination
                rowsPerPageOptions={[5, 10, 25]}
                count={rows.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
              />
            </TableRow>
          </TableFooter>
        </Table>
      </TableContainer>
      <Box sx={{ p: 2 }}>
        <FormControlLabel
          control={<Switch checked={dense} onChange={(e) => setDense(e.target.checked)} />}
          label="Dense"
        />
      </Box>
    </Paper>
  );
};

export default FilteredTable;
