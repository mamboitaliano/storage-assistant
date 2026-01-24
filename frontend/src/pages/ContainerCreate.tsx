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
import { containersApi } from "../api";
import { useCallback, useEffect, useState } from "react";
import { useFloorRoomSelection } from "@/hooks/useFloorRoomSelection";
import { FloorSelector } from "@/components/FloorSelector";
import { RoomSelector } from "@/components/RoomSelector";

export default function ContainerCreate() {
    const [name, setName] = useState<string>("");
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

    const createContainer = async () => {
        if (!selectedRoomId || !name) {
            return;
        }

        try {
            setLoading(true);
            setError(null);
            const data = await containersApi.create({
                name,
                room_id: selectedRoomId,
            });

            if (data) {
                navigate(`/containers/${data.id}`);
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

    useEffect(() => {
        validateForm();
    }, [validateForm]);

    return (
        <div className="flex flex-col h-full">
            <PageHeader 
                title="New Container" 
                action={
                    <Button size="sm" onClick={() => navigate("/containers")}>
                        <XIcon /> Cancel
                    </Button>
                } 
            />
            <div className="flex-1 min-h-0 mt-6 overflow-auto max-w-md">
                <FieldGroup>
                    <FieldSet>
                        <Field>
                            <FieldLabel>Name (required)</FieldLabel>
                            <Input type="text" placeholder="Container name" value={name} onChange={(e) => setName(e.target.value)} />
                        </Field>
                        {showFloorsDropdown && <FloorSelector floors={floors} onValueChange={handleFloorChange} disabled={loading} />}
                        {showRoomsDropdown && <RoomSelector rooms={rooms} onValueChange={handleRoomChange}  disabled={loading} required />}
                    </FieldSet>
                </FieldGroup>
                {displayError && (
                    <p className="text-sm text-red-500 mt-4">{displayError.message}</p>
                )}
            </div>
            <div className="flex justify-end mt-4">
                <Button
                    onClick={createContainer}
                    disabled={loading || !formValid}
                >
                    {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                    {loading ? "Creating..." : "Create"}
                </Button>
            </div>
        </div>
    )
};
