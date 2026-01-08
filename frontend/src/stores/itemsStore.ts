import { create } from "zustand";

export type ItemRowSelection = Record<string, boolean>;

interface ItemStore {
    rowSelection: ItemRowSelection;
    setRowSelection: (
        updater: ItemRowSelection | ((prev: ItemRowSelection) => ItemRowSelection)
    ) => void;
    clear: () => void;
};

export const useItemStore = create<ItemStore>(set => ({
    rowSelection: {},
    setRowSelection: updater =>
        set(state => ({
            rowSelection: typeof updater === 'function' ? updater(state.rowSelection) : updater,
        })),
    clear: () => set({ rowSelection: {} }),
}));