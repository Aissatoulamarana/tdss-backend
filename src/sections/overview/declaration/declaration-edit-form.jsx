import { z as zod } from 'zod';
import { useMemo } from 'react';
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
import { DeclarationEdit } from './declaration-edit';

// ----------------------------------------------------------------------

export const NewInvoiceSchema = zod.object({
  items: zod.array(
    zod.object({
      nom: zod.string().min(1, { message: 'Title is required!' }),
      nationalité: zod.string().min(1, { message: 'Service is required!' }),
      service: zod.string().min(1, { message: 'Service is required!' }),
      // Not required
    })
  ),
  // Not required

  status: zod.string(),
  invoiceNumber: zod.string(),
});

// ----------------------------------------------------------------------

export function DeclarationEditForm({ currentInvoice }) {
  const router = useRouter();

  const loadingSave = useBoolean();

  const loadingSend = useBoolean();

  const defaultValues = useMemo(
    () => ({
      invoiceNumber: currentInvoice?.invoiceNumber || 'INV-1990',
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
      reset();
      loadingSend.onFalse();
      router.push(paths.dashboard.declaration.root);
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

        <DeclarationEdit />
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
    </Form>
  );
}
