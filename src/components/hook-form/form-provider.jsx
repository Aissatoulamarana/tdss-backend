import { FormProvider as RHFProvider } from 'react-hook-form';

export function Form({ children, onSubmit, methods }) {
  return (
    <RHFProvider {...methods}>
      <form onSubmit={onSubmit} noValidate autoComplete="off">
        {children}
      </form>
    </RHFProvider>
  );
}