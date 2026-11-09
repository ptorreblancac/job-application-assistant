export default function StatCard({ title, value }) {
    return(
        <section className="stat-card">
            <h3 className="stat-title">{title}</h3>
            <p className="stat-value">{value}</p>
        </section>
    )
}