import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import PageHeader from "@/components/PageHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { containersApi, roomsApi } from "@/api";
import { useApi } from "@/hooks/useApi";
import { RoomSelector } from "@/components/RoomSelector";
import type { RoomOption } from "@/api";

export default function ContainerDetail() {
    const [editing, setEditing] = useState(false);
    const [allRooms, setAllRooms] = useState<RoomOption[] | null>(null);
    const [pendingName, setPendingName] = useState<string>("");
    const [pendingRoomId, setPendingRoomId] = useState<number | null>(null);

    const navigate = useNavigate();
    const { id } = useParams();
    const { data, loading, error: _error, refetch } = useApi(() => containersApi.get(Number(id)));
    
    const originalRoom = data?.room;
    const displayRooms = editing && allRooms
        ? allRooms
        : originalRoom
            ? [originalRoom]
            : [];

    // Initialize pending values when data loads
    useEffect(() => {
        if (data) {
            setPendingName(data.name || "");
            setPendingRoomId(data.room_id ?? null);
        }
    }, [data]);

    // Load all rooms when entering edit mode
    const toggleEditMode = async () => {
        if (!allRooms) {
            const response = await roomsApi.listAll();
            setAllRooms(response.data);
        }
        setEditing(true);
    };

    // Save changes
    const handleSave = async () => {
        const updates: { name?: string; room_id?: number | null } = {};
        
        if (pendingName !== data?.name) {
            updates.name = pendingName;
        }
        if (pendingRoomId !== data?.room_id) {
            updates.room_id = pendingRoomId;
        }
        
        if (Object.keys(updates).length > 0) {
            await containersApi.update(Number(id), updates);
            refetch();
        }

        setEditing(false);
    };

    // Discard pending changes
    const handleCancel = () => {
        setPendingName(data?.name || "");
        setPendingRoomId(data?.room_id ?? null);
        setAllRooms(null);
        setEditing(false);
    };

    // Handle room change
    const handleRoomValueChange = (value: string) => {
        setPendingRoomId(value ? parseInt(value) : null);
    };

    return (
        <div className="flex flex-col h-full">
            <PageHeader
                title={loading ? 'Loading...' : (data?.name || 'Unnamed Container')}
                action={
                    editing ? (
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
                            <Button size="sm" onClick={() => navigate('/containers')}>
                                All Containers
                            </Button>
                        </div>
                    )
                }
            />
            <div className="flex-1 min-h-0 mt-6 overflow-auto max-w-md space-y-4">
                {/* Name input - only in edit mode */}
                {editing && (
                    <div className="space-y-2">
                        <Label htmlFor="container-name">Container name</Label>
                        <Input
                            id="container-name"
                            value={pendingName}
                            onChange={(e) => setPendingName(e.target.value)}
                            placeholder="Enter container name"
                        />
                    </div>
                )}

                {/* Item count display */}
                <div className="text-sm text-muted-foreground">
                    {data?.item_count ?? 0} item{data?.item_count !== 1 ? 's' : ''} in this container
                </div>

                {/* Room selector */}
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
            </div>
        </div>
    );
}
