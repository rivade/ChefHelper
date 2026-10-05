export const AUTH0_ROLES_CLAIM = "https://chefhelper.app/roles";

export function hasAdminRole(user: unknown): boolean {
	if (!user || typeof user !== "object") return false;

	const roles = (user as Record<string, unknown>)[AUTH0_ROLES_CLAIM];
	return Array.isArray(roles) && roles.some((role) => role === "admin");
}