import { useNavigate } from 'react-router-dom';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import { MoreHorizontal } from 'lucide-react';
import type { Floor} from '@/api';
import { floorsApi } from '@/api';

export default function FloorDropdown({ floor }: { floor: Floor }) {
    const navigate = useNavigate();

    const handleDelete = async (id: number) => {
        try {
            await floorsApi.delete(id);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="text-right">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" aria-label="Open actions" className="h-8 w-8 p-0">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-36">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => navigate(`/floors/${floor.id}`)}>View Details</DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleDelete(floor.id)}>Delete</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
    )
};