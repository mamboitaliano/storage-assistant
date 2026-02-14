import { useCallback, useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import PageHeader from "@/components/PageHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { itemsApi, roomsApi } from "@/api";
import { useApi } from "@/hooks/useApi";
import { RoomSelector } from "@/components/RoomSelector";
import { ContainerSelector } from "@/components/ContainerSelector";
import AsyncSingleSelect, { type SelectOption } from "@/components/AsyncSingleSelect";
import type { RoomOption, ContainerOption } from "@/api";

export default function ItemDetail() {
    const [editing, setEditing] = useState(false);
    const [allRooms, setAllRooms] = useState<RoomOption[] | null>(null);
    const [pendingName, setPendingName] = useState<string>("");
    const [pendingRoomId, setPendingRoomId] = useState<number | null>(null);
    const [pendingContainer, setPendingContainer] = useState<SelectOption | null>(null);
    
    // Containers for the selected room
    const [roomContainers, setRoomContainers] = useState<ContainerOption[]>([]);
    const [loadingContainers, setLoadingContainers] = useState(false);

    const navigate = useNavigate();
    const { id } = useParams();
    const { data, loading, error: _error, refetch } = useApi(() => itemsApi.get(Number(id)));
    
    const originalRoom = data?.room;
    const displayRooms = editing && allRooms
        ? allRooms
        : originalRoom
            ? [data.room]
            : [];

    // Initialize pending values when data loads
    useEffect(() => {
        if (data) {
            setPendingName(data.name || "");
            setPendingRoomId(data.room_id);
            setPendingContainer(data.container 
                ? { id: data.container.id, name: data.container.name } 
                : null
            );
        }
    }, [data]);

    // Load containers when room changes (in edit mode)
    useEffect(() => {
        if (pendingRoomId && editing) {
            setLoadingContainers(true);
            roomsApi.listContainers(pendingRoomId)
                .then(setRoomContainers)
                .catch(console.error)
                .finally(() => setLoadingContainers(false));
        }
    }, [pendingRoomId, editing]);

    // Local search function - filters containers for the selected room
    const searchContainers = useCallback(async (query: string): Promise<SelectOption[]> => {
        if (!query.trim()) {
            return roomContainers;
        }
        const lowerQuery = query.toLowerCase();
        return roomContainers.filter(c => c.name?.toLowerCase().includes(lowerQuery));
    }, [roomContainers]);
    
    // Load all rooms when entering edit mode, then enable edit mode
    const toggleEditMode = async () => {
        if (!allRooms) {
            const response = await roomsApi.listAll();
            setAllRooms(response.data);
        }
        setEditing(true);
    };

    // Save changes
    const handleSave = async () => {
        const updates: { name?: string; room_id?: number; container_id?: number } = {};
        
        if (pendingName !== data?.name) {
            updates.name = pendingName;
        }
        if (pendingRoomId !== data?.room_id) {
            updates.room_id = pendingRoomId ?? undefined;
        }
        if (pendingContainer?.id !== data?.container_id) {
            updates.container_id = pendingContainer?.id ?? undefined;
        }
        
        if (Object.keys(updates).length > 0) {
            await itemsApi.update(Number(id), updates);
            refetch();
        }

        setEditing(false);
    };

    // Discard pending changes
    const handleCancel = () => {
        setPendingName(data?.name || "");
        setPendingRoomId(data?.room_id ?? null);
        setPendingContainer(data?.container ? { id: data.container.id, name: data.container.name } : null);
        setAllRooms(null);
        setEditing(false);
    };

    // Reset container when room changes
    const handleRoomValueChange = (value: string) => {
        setPendingRoomId(parseInt(value));
        setPendingContainer(null);
    };

    // Set pending container when container changes
    const handleContainerChange = (container: SelectOption | null) => {
        setPendingContainer(container);
    };

    return (
        <div className="flex flex-col h-full">
            <PageHeader
                title={loading ? 'Loading...' : (data?.name || 'Unnamed Item')}
                action={
                    editing ?
                    (
                        <div className="flex gap-2">
                            <Button size="sm" onClick={handleSave}>
                                Save
                            </Button>
                            <Button size="sm" onClick={handleCancel}>
                                Cancel
                            </Button>
                        </div>
                    ) : (
                        <div className="flex gap-2">
                            <Button size="sm" onClick={toggleEditMode}>
                                Edit
                            </Button>
                            <Button size="sm" onClick={() => navigate('/items')}>
                                All Items
                            </Button>
                        </div>
                    )
                }
            />
            <div className="flex-1 min-h-0 mt-6 overflow-auto max-w-md space-y-4">
                {/* Name input - only in edit mode */}
                {editing && (
                    <div className="space-y-2">
                        <Label htmlFor="item-name">Item name</Label>
                        <Input
                            id="item-name"
                            value={pendingName}
                            onChange={(e) => setPendingName(e.target.value)}
                            placeholder="Enter item name"
                        />
                    </div>
                )}

                <div>
                    <RoomSelector
                        value={pendingRoomId?.toString() ?? ""}
                        rooms={displayRooms}
                        onValueChange={handleRoomValueChange}
                        disabled={loading || !editing}
                    />
                    {!editing && pendingRoomId && (
                        <Link 
                            to={`/rooms/${pendingRoomId}`}
                            className="text-xs text-muted-foreground hover:text-foreground underline mt-1 inline-block"
                        >
                            View room
                        </Link>
                    )}
                </div>
                
                {/* Container selector - simple dropdown in view mode, searchable in edit mode */}
                <div>
                    {editing ? (
                        <AsyncSingleSelect
                            searchFn={searchContainers}
                            value={pendingContainer}
                            onChange={handleContainerChange}
                            placeholder={loadingContainers ? "Loading containers..." : "Search containers..."}
                            label="Container"
                            debounceMs={0}
                            minSearchLength={0}
                            disabled={loading || loadingContainers}
                        />
                    ) : (
                        <ContainerSelector
                            value={pendingContainer?.id?.toString() ?? ""}
                            containers={pendingContainer ? [pendingContainer] : []}
                            onValueChange={() => {}}
                            disabled={true}
                            placeholder={pendingContainer ? undefined : "None"}
                        />
                    )}
                    {!editing && pendingContainer && (
                        <Link 
                            to={`/containers/${pendingContainer.id}`}
                            className="text-xs text-muted-foreground hover:text-foreground underline mt-1 inline-block"
                        >
                            View container
                        </Link>
                    )}
                </div>
            </div>
        </div>
    )
};