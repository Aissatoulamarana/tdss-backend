import { z as zod } from 'zod';
import { useMemo } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import axios from 'axios';
import Card from '@mui/material/Card';
import Stack from '@mui/material/Stack';
import LoadingButton from '@mui/lab/LoadingButton';

import { paths } from 'src/routes/paths';
import { useRouter } from 'src/routes/hooks';

import { useBoolean } from 'src/hooks/use-boolean';

import { today, fIsAfter } from 'src/utils/format-time';

import { _addressBooks } from 'src/_mock';

import { Form, schemaHelper } from 'src/components/hook-form';

import { DeclarationEditStatusDate } from './declaration-status-edit';
import { DeclarationNewEditDetails } from './declaration-edit-detail';

// ----------------------------------------------------------------------

export const NewInvoiceSchema = zod.object({
  createDate: schemaHelper.date({
    message: { required_error: 'Create date is required!' },
  }),

  items: zod.array(
    zod.object({
      numero: zod.number().min(1, { message: 'Numero du passeport obligatoire' }),
      type: zod.string().min(1, { message: 'Title is required!' }),
      fonction: zod.string().min(1, { message: 'le champ fonction est obligatoire!' }),
      nationalite: zod.string().min(1, { message: "Selectionnez votre paus d'origine " }),
      // Not required
      prenom: zod.string().min(1, { message: 'Entrez votre prenom ' }),
      nom: zod.string().min(1, { message: 'Entrez votre nom ' }),
    })
  ),
  // Not required

  status: zod.string(),

  declarationNumber: zod.string(),
});

const generateUniqueId = () => {
  return 'DEC-' + Math.random().toString(36).substr(2, 9).toUpperCase();
};

// ----------------------------------------------------------------------

export function DeclarationNew({ currentInvoice }) {
  const router = useRouter();

  const loadingSave = useBoolean();

  const loadingSend = useBoolean();

  const defaultValues = useMemo(
    () => ({
      declarationNumber: currentInvoice?.declarationNumber || generateUniqueId(),
      createDate: currentInvoice?.createDate || today(),

      status: currentInvoice?.status || 'draft',

      items: currentInvoice?.items || [
        {
          numero: '',
          type: 'Nouvelle',
          nom: '',
          prenom: '',
          nationalite: '',
          fonction: '',
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
      router.push(paths.dashboard.declaration.list);
      console.info('DATA', JSON.stringify(data, null, 2));
    } catch (error) {
      console.error(error);
      loadingSave.onFalse();
    }
  });

  const handleCreateAndSend = handleSubmit(async (data) => {
    loadingSend.onTrue();

    try {
      // Ajouter le statut "soumise" à la donnée
      data.status = 'soumise';

      // Formater les champs de date si nécessaire (exemple: `created_at` ou `date_field`)
      if (data.date_field) {
        const date = new Date(data.date_field);
        data.date_field = date.toISOString().split('T')[0]; // Convertit en YYYY-MM-DD
      }

      // Simuler un délai pour des actions asynchrones (optionnel)
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Envoyer les données au backend via axios
      const response = await axios.post('http://127.0.0.1:8000/api/declarations/create/', data, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Afficher la réponse du backend dans la console (optionnel)
      console.log('Réponse du backend:', response.data);

      // Réinitialiser le formulaire après succès
      reset();

      // Arrêter le chargement
      loadingSend.onFalse();

      // Rediriger l'utilisateur
      router.push(paths.dashboard.declaration.list);
    } catch (error) {
      console.error("Erreur lors de l'envoi au backend:", error);

      // Arrêter le chargement en cas d'erreur
      loadingSend.onFalse();

      // Gérer les erreurs spécifiques
      if (error.response) {
        console.error('Erreur avec le serveur:', error.response.data);
      } else if (error.request) {
        console.error('Erreur avec la requête:', error.request);
      } else {
        console.error('Erreur générale:', error.message);
      }
    }
  });

  return (
    <Form methods={methods}>
      <Card>
        <DeclarationEditStatusDate />

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
          {currentInvoice ? 'Mettre A jour' : 'Soumettre'}
        </LoadingButton>
      </Stack>
    </Form>
  );
}
