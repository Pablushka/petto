// Keep frontend types aligned with backend models (backend/models.py)

// PetType enum values from backend
export type PetType = 'Cat' | 'Dog' | 'Lizard' | 'Hamster' | 'Bird' | 'Other';
export type PetStatus = 'at_home' | 'lost' | 'found';
// Minimal create payload shape expected by backend routers/pets.py
export interface PetCreate {
	owner_id: number;
	name: string;
	pet_type: PetType;
	picture: string;
	notes: string;
	status: PetStatus;
}

// PetOut mirrors backend PetOut pydantic model (includes id and owner relation as id)
export interface PetOut {
	id: number;
	owner_id: number; // Pydantic flattens FK to id by default in our usage
	name: string;
	pet_type: PetType;
	picture: string;
	notes: string;
	status: PetStatus;
}

// Update payload (backend expects the same fields as create for update validation)
export interface PetUpdate {
	owner_id: number;
	name: string;
	pet_type: PetType;
	picture?: string;
	notes: string;
	status: PetStatus;
}
