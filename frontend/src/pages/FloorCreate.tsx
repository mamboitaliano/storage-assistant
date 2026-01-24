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
import { floorsApi } from "@/api";
import { useCallback, useEffect, useState } from "react";

export default function FloorCreate() {
    const [name, setName] = useState<string>("");
    const [floorNumber, setFloorNumber] = useState<string>("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);
    const [formValid, setFormValid] = useState(false);

    const navigate = useNavigate();

    const createFloor = async () => {
        if (!name || !floorNumber) {
            return;
        }

        try {
            setLoading(true);
            setError(null);
            const data = await floorsApi.create({
                name,
                floor_number: parseInt(floorNumber),
            });

            if (data) {
                navigate(`/floors/${data.id}`);
            }
        } catch (e) {
            setError(e as Error);
        } finally {
            setLoading(false);
        }
    }

    const validateForm = useCallback(() => {
        setFormValid(Boolean(name && floorNumber));
    }, [name, floorNumber]);

    useEffect(() => {
        validateForm();
    }, [validateForm]);

    return (
        <div className="flex flex-col h-full">
            <PageHeader 
                title="New Floor" 
                action={
                    <Button size="sm" onClick={() => navigate("/floors")}>
                        <XIcon /> Cancel
                    </Button>
                } 
            />
            <div className="flex-1 min-h-0 mt-6 overflow-auto max-w-md">
                <FieldGroup>
                    <FieldSet>
                        <Field>
                            <FieldLabel>Name (required)</FieldLabel>
                            <Input type="text" placeholder="e.g. Ground Floor, Basement" value={name} onChange={(e) => setName(e.target.value)} />
                        </Field>
                        <Field>
                            <FieldLabel>Floor Number (required)</FieldLabel>
                            <Input type="number" placeholder="e.g. 0, 1, -1" value={floorNumber} onChange={(e) => setFloorNumber(e.target.value)} />
                        </Field>
                    </FieldSet>
                </FieldGroup>
                {error && (
                    <p className="text-sm text-red-500 mt-4">{error.message}</p>
                )}
            </div>
            <div className="flex justify-end mt-4">
                <Button
                    onClick={createFloor}
                    disabled={loading || !formValid}
                >
                    {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                    {loading ? "Creating..." : "Create"}
                </Button>
            </div>
        </div>
    )
};
