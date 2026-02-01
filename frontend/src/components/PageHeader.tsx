export default function PageHeader({ title, action }: { title: string, action?: React.ReactNode }) {
    return (
        <div
            className="flex flex-row justify-between items-center gap-4 pb-4 border-b"
            style={{ borderColor: 'var(--gunmetal-700)' }}
        >
            <h1
                className="text-xl font-semibold"
                style={{ color: 'var(--gunmetal-300)' }}
            >
                { title }
            </h1>
            {action && (
                <div className="flex justify-end items-center">
                    {action}
                </div>
            )}
        </div>
    );
};