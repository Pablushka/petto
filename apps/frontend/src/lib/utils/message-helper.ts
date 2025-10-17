/**
 * Temporary message helper to workaround Paraglide type issues
 *
 * This file provides a temporary solution to handle missing TypeScript types in the Paraglide message system.
 * Once the Paraglide type generation is fixed, this file should be removed and the original m.* functions used.
 */

import { m } from '$lib/paraglide/messages';

export type MessageKey =
	| 'pets_title'
	| 'pet_report_lost'
	| 'pet_report_found'
	| 'view_listings'
	| 'feature_report_title'
	| 'feature_report_description'
	| 'feature_found_title'
	| 'feature_found_description'
	| 'feature_browse_title'
	| 'feature_browse_description'
	| 'pet_filter_all'
	| 'pet_filter_lost'
	| 'pet_filter_found'
	| 'pet_filter_reunited'
	| 'pet_search_placeholder'
	| 'pet_status_lost'
	| 'pet_status_found'
	| 'pet_status_at_home'
	| 'pet_status_reunited'
	| 'pet_species'
	| 'pet_breed'
	| 'pet_gender'
	| 'pet_age'
	| 'pet_description'
	| 'pet_contact'
	| 'pet_location'
	| 'pet_details_title'
	| 'pet_date'
	| 'pet_last_seen'
	| 'pet_not_found'
	| 'pet_no_results'
	| 'pet_owner_contact'
	| 'pet_report_sighting'
	| 'pet_mark_reunited'
	| 'pet_no_contact_info'
	| 'pet_sighting_intro'
	| 'pet_name_label'
	| 'pet_report_error'
	| 'pet_report_success'
	| 'login_required'
	| 'pet_image_label'
	| 'back_to_list'
	| 'login_title'
	| 'login_button'
	| 'login_failed'
	| 'email_label'
	| 'password_label'
	| 'forgot_password_link'
	| 'forgot_title'
	| 'forgot_button'
	| 'forgot_success'
	| 'forgot_failed'
	| 'network_error'
	| 'loading'
	| 'auth_test_title'
	| 'session_greeting'
	| 'session_invalid'
	| 'session_not_logged_in'
	| 'logout_button'
	| 'button_submit'
	| 'button_cancel'
	| 'nav_home'
	| 'nav_pets'
	| 'nav_auth_test'
	| 'nav_demo'
	| 'add_new_pet'
	| 'pet_added_success'
	| 'reunite_lost_pets'
	| 'reunite_lost_pets_description'
	| 'all_rights_reserved'
	| 'edit_pet'
	| 'last_scan_location'
	| 'scan_location'
	| 'scan_time'
	| 'qr_link'
	| 'unknown_location'
	| 'pet_location_title'
	| 'back_to_pet'
	| 'no_scans_found'
	| 'print_flyer'
	| 'export_image'
	| 'edit_flyer'
	| 'finish_editing'
	| 'color_mode'
	| 'bw_mode';

// Fallback texts in case the message is missing
const fallbackMessages: Record<MessageKey, string> = {
	pets_title: 'Lost & Found Pets',
	pet_report_lost: 'Report Lost Pet',
	pet_report_found: 'Report Found Pet',
	view_listings: 'View Listings',
	feature_report_title: 'Report a Lost Pet',
	feature_report_description:
		'Create a listing for your lost pet with details and photos so the community can help.',
	feature_found_title: 'Report a Found Pet',
	feature_found_description:
		'Found a pet wandering? Share when and where you found them to help locate the owner.',
	feature_browse_title: 'Browse Listings',
	feature_browse_description:
		'Search lost and found pet posts near you and help reunite pets with their families.',
	pet_filter_all: 'All Pets',
	pet_filter_lost: 'Lost Pets',
	pet_filter_found: 'Found Pets',
	pet_filter_reunited: 'Reunited',
	pet_search_placeholder: 'Search by location, species, or description',
	pet_status_lost: 'Lost',
	pet_status_found: 'Found',
	pet_status_at_home: 'At home',
	pet_status_reunited: 'Reunited',
	pet_species: 'Species',
	pet_breed: 'Breed',
	pet_gender: 'Gender',
	pet_age: 'Age',
	pet_description: 'Description',
	pet_contact: 'Contact',
	pet_location: 'Location',
	pet_details_title: 'Pet Details',
	pet_date: 'Date',
	pet_last_seen: 'Last seen',
	pet_not_found: 'Pet not found',
	pet_no_results: 'No pets found matching your search',
	pet_owner_contact: 'Contact Owner',
	pet_report_sighting: 'Report Sighting',
	pet_mark_reunited: 'Mark as Reunited',
	pet_no_contact_info: 'No contact information available',
	pet_sighting_intro:
		'Have you seen this pet? Please provide details about when and where you spotted it.',
	pet_name_label: 'Name',
	pet_report_error: 'Error reporting pet',
	pet_report_success: 'Pet reported successfully!',
	login_required: 'You must be logged in to report a pet',
	pet_image_label: 'Upload Image',
	back_to_list: 'Back to List',
	login_title: 'Sign in',
	login_button: 'Sign in',
	login_failed: 'Incorrect credentials',
	email_label: 'Email',
	password_label: 'Password',
	forgot_password_link: 'Forgot your password?',
	forgot_title: 'Password recovery',
	forgot_button: 'Send link',
	forgot_success: 'Check your email to recover your password!',
	forgot_failed: 'Could not send email',
	network_error: 'Network error',
	loading: 'Loading...',
	auth_test_title: 'Authentication test',
	session_greeting: 'Hello, {email}',
	session_invalid: 'Session invalid or expired',
	session_not_logged_in: 'You are not signed in',
	logout_button: 'Sign out',
	button_submit: 'Submit',
	button_cancel: 'Cancel',
	nav_home: 'Home',
	nav_pets: 'Pets',
	nav_auth_test: 'Auth Test',
	nav_demo: 'Demo',
	add_new_pet: 'Add New Pet',
	pet_added_success: 'Pet added successfully!',
	reunite_lost_pets: 'Reunite Lost Pets',
	reunite_lost_pets_description:
		'Help lost pets find their way home. Report lost pets, found pets, or browse listings to reunite pets with their owners.',
	all_rights_reserved: 'All rights reserved',
	edit_pet: 'Edit Pet',
	last_scan_location: 'Last Scan Location',
	scan_location: 'Location',
	scan_time: 'Time',
	qr_link: 'QR Link',
	unknown_location: 'Unknown location',
	pet_location_title: 'Pet Location',
	back_to_pet: 'Back to Pet',
	no_scans_found: 'No scans found for this pet',
	print_flyer: 'Print Flyer',
	export_image: 'Export as Image',
	edit_flyer: 'Edit Flyer',
	finish_editing: 'Finish Editing',
	color_mode: 'Color Mode',
	bw_mode: 'B&W Mode'
};

/**
 * A type-safe message getter that falls back to English if the message is missing
 * @param key The message key
 * @param params Optional parameters for the message
 * @returns The translated message or fallback text
 */
export function getMessage(key: MessageKey, params?: Record<string, string>): string {
	// Direct property access using type assertion - avoids TypeScript errors

	const messageFunc = m as unknown as Record<
		MessageKey,
		(params?: Record<string, string>) => string
	>;

	try {
		if (typeof messageFunc[key] === 'function') {
			return messageFunc[key](params);
		}
		return fallbackMessages[key];
	} catch {
		// Fall back to English if the message is not available
		return fallbackMessages[key];
	}
}
