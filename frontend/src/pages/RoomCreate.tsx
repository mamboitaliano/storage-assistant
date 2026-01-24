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
import { floorsApi, roomsApi, type Floor } from "@/api";
import { useCallback, useEffect, useState } from "react";
import { FloorSelector } from "@/components/FloorSelector";

export default function RoomCreate() {
    const [showFloorsDropdown, setShowFloorsDropdown] = useState(false);
    const [floors, setFloors] = useState<Floor[] | null>(null);
    const [name, setName] = useState<string>("");
    const [selectedFloorId, setSelectedFloorId] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);
    const [formValid, setFormValid] = useState(false);

    const navigate = useNavigate();

    const createRoom = async () => {
        if (!selectedFloorId || !name) {
            return;
        }

        try {
            setLoading(true);
            setError(null);
            const data = await roomsApi.create({
                name,
                floor_id: selectedFloorId,
            });

            if (data) {
                navigate(`/rooms/${data.id}`);
            }
        } catch (e) {
            setError(e as Error);
        } finally {
            setLoading(false);
        }
    }

    const validateForm = useCallback(() => {
        setFormValid(Boolean(name && selectedFloorId));
    }, [name, selectedFloorId]);

    const loadFloors = async () => {
        try {
            const { data } = await floorsApi.list();
            setFloors(data || []);

            if (data && data.length > 1) {
                setShowFloorsDropdown(true);
            } else if (data && data.length === 1) {
                setSelectedFloorId(data[0].id);
            }
        } catch (e) {
            setError(e as Error);
        }
    }

    const handleFloorValueChange = (value: string) => {
        setSelectedFloorId(parseInt(value));
    }

    useEffect(() => {
        loadFloors();
    }, []);

    useEffect(() => {
        validateForm();
    }, [validateForm]);

    return (
        <div className="flex flex-col h-full">
            <PageHeader 
                title="New Room" 
                action={
                    <Button size="sm" onClick={() => navigate("/rooms")}>
                        <XIcon /> Cancel
                    </Button>
                } 
            />
            <div className="flex-1 min-h-0 mt-6 overflow-auto max-w-md">
                <FieldGroup>
                    <FieldSet>
                        <Field>
                            <FieldLabel>Name (required)</FieldLabel>
                            <Input type="text" placeholder="Room name" value={name} onChange={(e) => setName(e.target.value)} />
                        </Field>
                        {showFloorsDropdown && <FloorSelector floors={floors} onValueChange={handleFloorValueChange} disabled={loading} />}
                    </FieldSet>
                </FieldGroup>
                {error && (
                    <p className="text-sm text-red-500 mt-4">{error.message}</p>
                )}
            </div>
            <div className="flex justify-end mt-4">
                <Button
                    onClick={createRoom}
                    disabled={loading || !formValid}
                >
                    {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                    {loading ? "Creating..." : "Create"}
                </Button>
            </div>
        </div>
    )
};
