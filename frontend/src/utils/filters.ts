import type { ItemFilters, ContainerFilters } from "@/api";

/**
 * Compare two ItemFilters objects for equality.
 * Returns true if both filters have the same values.
 */
export function filtersAreEqual(
    a: ItemFilters | undefined, 
    b: ItemFilters | undefined
): boolean {
    const aName = a?.name || '';
    const bName = b?.name || '';
    const aRooms = a?.rooms || [];
    const bRooms = b?.rooms || [];
    const aContainers = a?.containers || [];
    const bContainers = b?.containers || [];
    
    if (aName !== bName) return false;
    if (aRooms.length !== bRooms.length) return false;
    if (aContainers.length !== bContainers.length) return false;
    if (!aRooms.every((id, i) => bRooms[i] === id)) return false;
    if (!aContainers.every((id, i) => bContainers[i] === id)) return false;
    
    return true;
}

/**
 * Compare two ContainerFilters objects for equality.
 * Returns true if both filters have the same values.
 */
export function containerFiltersAreEqual(
    a: ContainerFilters | undefined, 
    b: ContainerFilters | undefined
): boolean {
    const aName = a?.name || '';
    const bName = b?.name || '';
    const aRooms = a?.rooms || [];
    const bRooms = b?.rooms || [];
    
    if (aName !== bName) return false;
    if (aRooms.length !== bRooms.length) return false;
    if (!aRooms.every((id, i) => bRooms[i] === id)) return false;
    
    return true;
}
