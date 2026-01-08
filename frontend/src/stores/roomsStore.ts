import { create } from "zustand";

export type RoomRowSelection = Record<string, boolean>;

interface RoomStore {
    rowSelection: RoomRowSelection;
    setRowSelection: (
        updater: RoomRowSelection | ((prev: RoomRowSelection) => RoomRowSelection)
    ) => void;
    clear: () => void;
};

export const useRoomStore = create<RoomStore>(set => ({
    rowSelection: {},
    setRowSelection: updater =>
        set(state => ({
            rowSelection: typeof updater === 'function' ? updater(state.rowSelection) : updater,
        })),
    clear: () => set({ rowSelection: {} }),
}));