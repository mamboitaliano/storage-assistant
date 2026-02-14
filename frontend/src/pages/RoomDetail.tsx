import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import PageHeader from "@/components/PageHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { roomsApi } from "@/api";
import { useApi } from "@/hooks/useApi";

export default function RoomDetail() {
    const [editing, setEditing] = useState(false);
    const [pendingName, setPendingName] = useState<string>("");

    const navigate = useNavigate();
    const { id } = useParams();
    const { data, loading, error: _error, refetch } = useApi(() => roomsApi.get(Number(id)));

    // Initialize pending values when data loads
    useEffect(() => {
        if (data) {
            setPendingName(data.name || "");
        }
    }, [data]);

    // Enter edit mode
    const toggleEditMode = () => {
        setEditing(true);
    };

    // Save changes
    const handleSave = async () => {
        const updates: { name?: string } = {};
        
        if (pendingName !== data?.name) {
            updates.name = pendingName;
        }
        
        if (Object.keys(updates).length > 0) {
            await roomsApi.update(Number(id), updates);
            refetch();
        }

        setEditing(false);
    };

    // Discard pending changes
    const handleCancel = () => {
        setPendingName(data?.name || "");
        setEditing(false);
    };

    return (
        <div className="flex flex-col h-full">
            <PageHeader
                title={loading ? 'Loading...' : (data?.name || 'Unnamed Room')}
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
                            <Button size="sm" onClick={() => navigate('/rooms')}>
                                All Rooms
                            </Button>
                        </div>
                    )
                }
            />
            <div className="flex-1 min-h-0 mt-6 overflow-auto max-w-md space-y-4">
                {/* Name input - only in edit mode */}
                {editing && (
                    <div className="space-y-2">
                        <Label htmlFor="room-name">Room name</Label>
                        <Input
                            id="room-name"
                            value={pendingName}
                            onChange={(e) => setPendingName(e.target.value)}
                            placeholder="Enter room name"
                        />
                    </div>
                )}

                {/* Stats display */}
                <div className="space-y-2 text-sm text-muted-foreground">
                    <div>
                        {data?.item_count ?? 0} item{data?.item_count !== 1 ? 's' : ''} in this room
                    </div>
                    <div>
                        {data?.container_count ?? 0} container{data?.container_count !== 1 ? 's' : ''} in this room
                    </div>
                </div>
            </div>
        </div>
    );
}
