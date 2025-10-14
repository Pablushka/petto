// Utility helpers related to Pet entities
// Centralizes cover image selection and defaults so components remain consistent.

import type { PetOut } from '$lib/types/api/pet';

// Unified default image (ensure this exists in static or adjust path)
export const DEFAULT_PET_IMAGE = 'default_pet.jpg';

/**
 * Returns the best cover image url for a pet.
 * Priority:
 * 1. First element of pictures[] if non-empty.
 * 2. picture field (legacy / single image).
 * 3. DEFAULT_PET_IMAGE fallback.
 */
export function getPetCover(pet: Partial<PetOut> | undefined | null): string {
	if (!pet) return DEFAULT_PET_IMAGE;
	if (pet.pictures && pet.pictures.length > 0 && pet.pictures[0]) {
		return pet.pictures[0];
	}
	if (pet.picture) return pet.picture;
	return DEFAULT_PET_IMAGE;
}
