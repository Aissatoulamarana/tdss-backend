import { z as zod } from 'zod';

import { useState, useMemo } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import Card from '@mui/material/Card';
import Stack from '@mui/material/Stack';
import LoadingButton from '@mui/lab/LoadingButton';
import { paths } from 'src/routes/paths';
import { useRouter } from 'src/routes/hooks';
import { useBoolean } from 'src/hooks/use-boolean';
import { today, fIsAfter } from 'src/utils/format-time';
import { Form } from 'src/components/hook-form';
import { DeclarationNewEditStatusDate } from './declaration-status';
import { DeclarationNewEditDetails } from './declaration-edit-detail';
// import { DeclarationTableRow } from './view/declaration-list-view'; // Importation du composant Liste

export const NewInvoiceSchema = zod
  .object({
    createDate: zod.date({
      message: { required_error: 'Create date is required!' },
    }),
    items: zod.array(
      zod.object({
        nom: zod.string().min(1, { message: 'Title is required!' }),
        nationalité: zod.string().min(1, { message: 'Service is required!' }),
        service: zod.string().min(1, { message: 'Service is required!' }),
        price: zod.number(),
        total: zod.number(),
      })
    ),
    taxes: zod.number(),
    status: zod.string(),
    totalAmount: zod.number(),
    invoiceNumber: zod.string(),
  })
  .refine((data) => !fIsAfter(data.createDate, data.dueDate), {
    message: 'Due date cannot be earlier than create date!',
    path: ['dueDate'],
  });

const generateUniqueId = () => {
  return 'DEC-' + Math.random().toString(36).substr(2, 9).toUpperCase();
};

export function DeclarationNew({ currentInvoice }) {
  const router = useRouter();
  const loadingSave = useBoolean();
  const loadingSend = useBoolean();
  const [submissions, setSubmissions] = useState([]); // État pour les soumissions

  const defaultValues = useMemo(
    () => ({
      invoiceNumber: currentInvoice?.invoiceNumber || generateUniqueId(),
      createDate: currentInvoice?.createDate || today(),
      status: currentInvoice?.status || 'draft',
      discount: currentInvoice?.discount || 0,
      totalAmount: currentInvoice?.totalAmount || 0,
      items: currentInvoice?.items || [
        {
          nom: '',
          nationalité: '',
          service: '',
          price: 0,
          total: 0,
        },
      ],
    }),
    [currentInvoice]
  );

  const methods = useForm({
    mode: 'all',
    resolver: zodResolver(NewInvoiceSchema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleSaveAsDraft = handleSubmit(async (data) => {
    loadingSave.onTrue();

    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      setSubmissions([...submissions, { ...data, status: 'Brouillon' }]);
      reset();
      loadingSave.onFalse();
      router.push(paths.dashboard.invoice.root);
      console.info('DATA', JSON.stringify(data, null, 2));
    } catch (error) {
      console.error(error);
      loadingSave.onFalse();
    }
  });

  const handleCreateAndSend = handleSubmit(async (data) => {
    loadingSend.onTrue();

    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      setSubmissions([...submissions, { ...data, status: 'En attente de validation' }]);
      reset();
      loadingSend.onFalse();
      router.push(paths.dashboard.declaration.list);
      console.info('DATA', JSON.stringify(data, null, 2));
    } catch (error) {
      console.error(error);
      loadingSend.onFalse();
    }
  });

  return (
    <Form methods={methods}>
      <Card>
        <DeclarationNewEditStatusDate />

        <DeclarationNewEditDetails />
      </Card>
      <Stack justifyContent="flex-end" direction="row" spacing={2} sx={{ mt: 3 }}>
        <LoadingButton
          color="inherit"
          size="large"
          variant="outlined"
          loading={loadingSave.value && isSubmitting}
          onClick={handleSaveAsDraft}
        >
          Brouillon
        </LoadingButton>

        <LoadingButton
          size="large"
          variant="contained"
          loading={loadingSend.value && isSubmitting}
          onClick={handleCreateAndSend}
        >
          {currentInvoice ? 'Mettre à jour' : 'Créer'} & Soumettre
        </LoadingButton>
      </Stack>
      {/*  <DeclarationTableRow data={submissions} />{' '}
       Ajout du composant Liste pour afficher les soumissions */}
    </Form>
  );
}
