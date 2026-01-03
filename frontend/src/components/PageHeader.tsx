export default function PageHeader({ title }: { title: string }) {
    return (
        <div
            className="flex flex-col gap-4 pb-4 mb-6 border-b"
            style={{ borderColor: 'var(--gunmetal-700)' }}
        >
            <h1
                className="text-xl font-semibold"
                style={{ color: 'var(--gunmetal-300)' }}
            >
                { title }
            </h1>
        </div>
    );
};