import PageHeader from "@/components/PageHeader";
import { Button } from "@/components/ui/button"
import {
  Field,
  FieldGroup,
  FieldLabel,
  FieldSet,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { useNavigate } from "react-router-dom";
import { Loader2, XIcon } from "lucide-react";
import { roomsApi, type ContainerOption, itemsApi } from "@/api";
import { useCallback, useEffect, useState } from "react";
import { useFloorRoomSelection } from "@/hooks/useFloorRoomSelection";
import { FloorSelector } from "@/components/FloorSelector";
import { RoomSelector } from "@/components/RoomSelector";
import { ContainerSelector } from "@/components/ContainerSelector";

export default function ItemCreate() {
    const [showContainersDropdown, setShowContainersDropdown] = useState(false);
    const [containers, setContainers] = useState<ContainerOption[] | null>(null);
    const [name, setName] = useState<string>("");
    const [selectedContainerId, setSelectedContainerId] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);
    const [formValid, setFormValid] = useState(false);
    const {
        floors,
        rooms,
        selectedRoomId,
        showFloorsDropdown,
        showRoomsDropdown,
        handleFloorChange,
        handleRoomChange,
        error: selectionError,
    } = useFloorRoomSelection();

    const navigate = useNavigate();
    const displayError = error || selectionError;

    const createItem = async () => {
        if (!selectedRoomId || !name) {
            return;
        }

        try {
            setLoading(true);
            setError(null);
            const data = await itemsApi.create({
                name,
                room_id: selectedRoomId,
                container_id: selectedContainerId ?? undefined,
            });

            if (data) {
                navigate(`/items/${data.id}`);
            }
        } catch (e) {
            setError(e as Error);
        } finally {
            setLoading(false);
        }
    }

    const validateForm = useCallback(() => {
        setFormValid(Boolean(name && selectedRoomId));
    }, [name, selectedRoomId]);

    const loadContainers = async (roomId: number) => {
        try {
            const data = await roomsApi.listContainers(roomId);
            setContainers(data || []);
            setSelectedContainerId(null);

            if (data && data.length >= 1) {
                setShowContainersDropdown(true);
            }
        } catch (e) {
            setError(e as Error);
        }
    }

    const handleFloorValueChange = (value: string) => {
        setSelectedContainerId(null);
        setShowContainersDropdown(false);
        setContainers(null);
        handleFloorChange(value);
    }

    const handleRoomValueChange = (value: string) => {
        handleRoomChange(value);
        setShowContainersDropdown(false);
        setSelectedContainerId(null);
        setContainers(null);
        loadContainers(parseInt(value));
    }

    const handleContainerValueChange = (value: string) => {
        setSelectedContainerId(parseInt(value));
    }

    useEffect(() => {
        validateForm();
    }, [validateForm]);

    return (
        <div className="flex flex-col h-full">
            <PageHeader 
                title="New Item" 
                action={
                    <Button size="sm" onClick={() => navigate("/items")}>
                        <XIcon /> Cancel
                    </Button>
                } 
            />
            <div className="flex-1 min-h-0 mt-6 overflow-auto max-w-md">
                <FieldGroup>
                    <FieldSet>
                        <Field>
                            <FieldLabel>Name (required)</FieldLabel>
                            <Input type="text" placeholder="Item name" value={name} onChange={(e) => setName(e.target.value)} />
                        </Field>
                        {showFloorsDropdown && <FloorSelector floors={floors} onValueChange={handleFloorValueChange} disabled={loading} />}
                        {showRoomsDropdown && <RoomSelector rooms={rooms} onValueChange={handleRoomValueChange} disabled={loading} required />}
                        {showContainersDropdown && <ContainerSelector containers={containers} onValueChange={handleContainerValueChange} disabled={loading} />}
                    </FieldSet>
                </FieldGroup>
                {displayError && (
                    <p className="text-sm text-red-500 mt-4">{displayError.message}</p>
                )}
            </div>
            <div className="flex justify-end mt-4">
                <Button
                    onClick={createItem}
                    disabled={loading || !formValid}
                >
                    {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                    {loading ? "Creating..." : "Create"}
                </Button>
            </div>
        </div>
    )
};
