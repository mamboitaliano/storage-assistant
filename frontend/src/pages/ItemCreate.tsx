import PageHeader from "@/components/PageHeader";
import { Button } from "@/components/ui/button"
import {
  Field,
  FieldGroup,
  FieldLabel,
  FieldSet,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useNavigate } from "react-router-dom";
import { Loader2, XIcon } from "lucide-react";
import { floorsApi, roomsApi, type Floor, type RoomOption, type ContainerOption, itemsApi } from "../api";
import { useCallback, useEffect, useState } from "react";

export default function ItemCreate() {
    const [showFloorsDropdown, setShowFloorsDropdown] = useState(false);
    const [showRoomsDropdown, setShowRoomsDropdown] = useState(false);
    const [showContainersDropdown, setShowContainersDropdown] = useState(false);
    const [floors, setFloors] = useState<Floor[] | null>(null);
    const [rooms, setRooms] = useState<RoomOption[] | null>(null);
    const [containers, setContainers] = useState<ContainerOption[] | null>(null);
    const [name, setName] = useState<string>("");
    const [selectedRoomId, setSelectedRoomId] = useState<number | null>(null);
    const [selectedContainerId, setSelectedContainerId] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);
    const [formValid, setFormValid] = useState(false);

    const navigate = useNavigate();

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

    const loadFloors = async () => {
        try {
            const { data } = await floorsApi.list();
            setFloors(data || []);
            setSelectedRoomId(null);
            setSelectedContainerId(null);

            if (data && data.length > 1) {
                setShowFloorsDropdown(true);
            } else if (data && data.length === 1) {
                loadRooms(data[0].id);
            }
        } catch (e) {
            setError(e as Error);
        }
    }

    const loadRooms = async (floorId: number) => {
        try {
            const data = await floorsApi.listRooms(floorId);
            setRooms(data || []);
            setSelectedContainerId(null);

            if (data && data.length > 1) {
                setSelectedRoomId(null);
                setShowRoomsDropdown(true);
            } else if (data && data.length === 1) {
                setSelectedRoomId(data[0].id);
                loadContainers(data[0].id);
            }
        } catch (e) {
            setError(e as Error);
        }
    }

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
        setSelectedRoomId(null);
        setSelectedContainerId(null);
        setShowRoomsDropdown(false);
        setShowContainersDropdown(false);
        setContainers(null);
        setRooms(null);
        loadRooms(parseInt(value));
    }

    const handleRoomValueChange = (value: string) => {
        setShowContainersDropdown(false);
        setSelectedRoomId(parseInt(value));
        setSelectedContainerId(null);
        setContainers(null);
        loadContainers(parseInt(value));
    }

    const handleContainerValueChange = (value: string) => {
        setSelectedContainerId(parseInt(value));
    }

    useEffect(() => {
        loadFloors();
    }, []);

    useEffect(() => {
        validateForm();
    }, [validateForm]);

    const renderFloorsDropdown = () => {
        if (!showFloorsDropdown) {
            return null;
        }

        return (
            <Field>
                <FieldLabel>Floor</FieldLabel>
                <Select onValueChange={handleFloorValueChange} disabled={loading}>
                    <SelectTrigger>
                        <SelectValue placeholder="Select a floor" />
                    </SelectTrigger>
                    <SelectContent position="item-aligned">
                        {floors?.map((floor) => (
                            <SelectItem key={floor.id} value={floor.id.toString()}>{floor.name}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </Field>
        )
    }

    const renderRoomsDropdown = () => {
        return (
            <Field>
                <FieldLabel>Room (required)</FieldLabel>
                <Select onValueChange={handleRoomValueChange} disabled={loading}>
                    <SelectTrigger>
                        <SelectValue placeholder="Select a room" />
                    </SelectTrigger>
                    <SelectContent position="item-aligned">
                        {rooms?.map((room) => (
                            <SelectItem key={room.id} value={room.id.toString()}>{room.name}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </Field>
        )
    }

    const renderContainersDropdown = () => {
        return (
            <Field>
                <FieldLabel>Container (optional)</FieldLabel>
                <Select onValueChange={handleContainerValueChange} disabled={loading}>
                    <SelectTrigger>
                        <SelectValue placeholder="Select a container" />
                    </SelectTrigger>
                    <SelectContent position="item-aligned">
                        {containers?.map((container) => (
                            <SelectItem key={container.id} value={container.id.toString()}>{container.name}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </Field>
        )
    }

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
                        {renderFloorsDropdown()}
                        {showRoomsDropdown && renderRoomsDropdown()}
                        {showContainersDropdown && renderContainersDropdown()}
                    </FieldSet>
                </FieldGroup>
                {error && (
                    <p className="text-sm text-red-500 mt-4">{error.message}</p>
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
