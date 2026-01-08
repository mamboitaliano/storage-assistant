import { create } from "zustand";

export type FloorRowSelection = Record<string, boolean>;

interface FloorStore {
	rowSelection: FloorRowSelection;
	setRowSelection: (
		updater: FloorRowSelection | ((prev: FloorRowSelection) => FloorRowSelection)
	) => void;
	clear: () => void;
};

export const useFloorStore = create<FloorStore>(set => ({
	rowSelection: {},
	setRowSelection: updater =>
		set(state => ({
			rowSelection: typeof updater === 'function' ? updater(state.rowSelection) : updater,
		})),  
	clear: () => set({ rowSelection: {} }),
}));