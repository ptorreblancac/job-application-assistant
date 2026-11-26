import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import JobCard from '../components/JobCard'

describe('JobCard', () => {
    it('displays the job information', () => {
        render(
            <JobCard
                title="Software Engineer"
                company="Google"
                location="Barcelona"
                employmentType="Full-time"
                match={85}
                datePosted="2026-11-20"
            />
        )

        expect(screen.getByText('Software Engineer')).toBeInTheDocument()
        expect(screen.getByText(/Google/)).toBeInTheDocument()
        expect(screen.getByText(/Barcelona/)).toBeInTheDocument()
    })

    it('displays the match score', () => {
        render(
            <JobCard
                title="Software Engineer"
                company="Google"
                location="Barcelona"
                match={85}
            />
        )

        expect(screen.getByText('85/100')).toBeInTheDocument()
    })

    it('displays Not scored when match is null', () => {
        render(
            <JobCard
                title="Software Engineer"
                company="Google"
                location="Barcelona"
                match={null}
            />
        )

        expect(screen.getByText('Not scored')).toBeInTheDocument()
    })

    it('displays Not specified when employment type is missing', () => {
        render(
            <JobCard
                title="Software Engineer"
                company="Google"
                location="Barcelona"
            />
        )

        expect(screen.getByText(/Not specified/)).toBeInTheDocument()
    })

    it('displays Date unknown when posting date is missing', () => {
        render(
            <JobCard
                title="Software Engineer"
                company="Google"
                location="Barcelona"
            />
        )

        expect(screen.getByText(/Date unknown/)).toBeInTheDocument()
    })

    it('displays the formatted posting date', () => {
        render(
            <JobCard
                title="Software Engineer"
                company="Google"
                location="Barcelona"
                datePosted="2026-11-20"
            />
        )

        const formattedDate = new Date("2026-11-20").toLocaleDateString()

        expect(screen.getByText(new RegExp(formattedDate))).toBeInTheDocument()
    })

    it('renders the job title as a link when posting link is provided', () => {
        render(
            <JobCard
                title="Software Engineer"
                company="Google"
                location="Barcelona"
                postingLink="https://example.com/job"
            />
        )

        const link = screen.getByRole('link', { name: 'Software Engineer' })

        expect(link).toHaveAttribute('href', 'https://example.com/job')
        expect(link).toHaveAttribute('target', '_blank')
    })

    it('renders the job title as plain text when posting link is missing', () => {
        render(
            <JobCard
                title="Software Engineer"
                company="Google"
                location="Barcelona"
            />
        )

        expect(screen.getByText('Software Engineer')).toBeInTheDocument()
        expect(screen.queryByRole('link')).not.toBeInTheDocument()
    })

    it('adds secure attributes to the external posting link', () => {
        render(
            <JobCard
                title="Software Engineer"
                company="Google"
                location="Barcelona"
                postingLink="https://example.com/job"
            />
        )

        const link = screen.getByRole('link', { name: 'Software Engineer' })

        expect(link).toHaveAttribute('rel', 'noopener noreferrer')
    })
})
