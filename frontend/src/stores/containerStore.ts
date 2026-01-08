import { create } from "zustand";

export type ContainerRowSelection = Record<string, boolean>;

interface ContainerStore {
  	rowSelection: ContainerRowSelection;
  	setRowSelection: (
    	updater: ContainerRowSelection | ((prev: ContainerRowSelection) => ContainerRowSelection)
  	) => void;
  	clear: () => void;
};

export const useContainerStore = create<ContainerStore>(set => ({
  	rowSelection: {},
  	setRowSelection: updater =>
    	set(state => ({
      		rowSelection: typeof updater === 'function' ? updater(state.rowSelection) : updater,
    	})),
  	clear: () => set({ rowSelection: {} }),
}));


