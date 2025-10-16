// define PetLocationScan type
export interface PetLocationScan {
	pet_id: number;
	user_id: number;
	scan_location?: string;
	scan_time: string;
	qr_link: string;
}
