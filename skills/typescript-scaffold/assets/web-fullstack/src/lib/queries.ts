import { useQuery } from '@tanstack/react-query';
import { api, fetchJson } from '@/lib/api';

// Server data the pages share. Query keys: ['items'].

export function useItems() {
  return useQuery({ queryKey: ['items'], queryFn: () => fetchJson(api.items.$get()) });
}
