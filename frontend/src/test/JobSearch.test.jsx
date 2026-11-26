
import { render, screen } from '@testing-library/react'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import userEvent from '@testing-library/user-event'
import JobSearch from '../components/JobSearch'

const mockJobs = [
    {
        id: 1,
        title: 'Junior Software Engineer',
        company: 'Google',
        location: 'Barcelona',
        job_type: 'Full-time',
        description: 'Backend development with Python',
        relevance_score: 80,
        date_posted: '2026-01-01',
        posting_link: 'https://example.com/1'
    },
    {
        id: 2,
        title: 'Frontend Developer',
        company: 'Amazon',
        location: 'Madrid',
        job_type: 'Part-time',
        description: 'React and JavaScript development',
        relevance_score: 95,
        date_posted: '2026-01-02',
        posting_link: 'https://example.com/2'
    },
    {
        id: 3,
        title: 'Backend Developer',
        company: 'Google',
        location: 'Madrid',
        job_type: 'Full-time',
        description: 'Django and PostgreSQL',
        relevance_score: null,
        date_posted: '2026-01-03',
        posting_link: 'https://example.com/3'
    }
]

describe('JobSearch', () => {
    beforeEach(() => {
        vi.stubGlobal('fetch', vi.fn().mockReturnValue(new Promise(() => {})))
    })

    const loadJobs = () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockJobs
        })
    }

    const renderLoadedJobs = async () => {
        loadJobs()
        render(<JobSearch />)

        await screen.findByText('Junior Software Engineer')
    }

    const getJobTitles = () => {
        return screen.getAllByRole('link').map(link => link.textContent)
    }

    // Initial state and API

    it('displays the loading message initially', () => {
        render(<JobSearch />)

        expect(screen.getByText('Loading jobs...')).toBeInTheDocument()
    })

    it('fetches jobs from the correct API endpoint', async () => {
        await renderLoadedJobs()

        expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/jobs/')
    })

    it('displays an error if the request fails', async () => {
        fetch.mockRejectedValue(new Error('Network error'))

        render(<JobSearch />)

        expect(await screen.findByText(
            'Unable to load jobs. Please try again later.'
        )).toBeInTheDocument()
    })

    it('displays an error if the response is unsuccessful', async () => {
        fetch.mockResolvedValue({ ok: false })

        render(<JobSearch />)

        expect(await screen.findByText(
            'Unable to load jobs. Please try again later.'
        )).toBeInTheDocument()
    })

    it('displays a message when there are no jobs', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => []
        })

        render(<JobSearch />)

        expect(await screen.findByText('No jobs found')).toBeInTheDocument()
    })

    // Job rendering and sorting

    it('displays all available jobs', async () => {
        await renderLoadedJobs()

        expect(screen.getByText('Junior Software Engineer')).toBeInTheDocument()
        expect(screen.getByText('Frontend Developer')).toBeInTheDocument()
        expect(screen.getByText('Backend Developer')).toBeInTheDocument()
    })

    it('sorts jobs by relevance score in descending order', async () => {
        await renderLoadedJobs()

        expect(getJobTitles()).toEqual([
            'Frontend Developer',
            'Junior Software Engineer',
            'Backend Developer'
        ])
    })

    it('places jobs without a relevance score last', async () => {
        await renderLoadedJobs()

        const titles = getJobTitles()

        expect(titles[titles.length - 1]).toBe('Backend Developer')
    })

    // Company filter

    it('filters jobs by company', async () => {
        const user = userEvent.setup()
        await renderLoadedJobs()

        await user.selectOptions(screen.getByRole('combobox', { name: 'Company' }), 'Amazon')

        expect(screen.getByText('Frontend Developer')).toBeInTheDocument()
        expect(screen.queryByText('Junior Software Engineer')).not.toBeInTheDocument()
        expect(screen.queryByText('Backend Developer')).not.toBeInTheDocument()
    })

    // Location filter

    it('filters jobs by location', async () => {
        const user = userEvent.setup()
        await renderLoadedJobs()

        await user.selectOptions(screen.getByRole('combobox', { name: 'Location' }), 'Barcelona')

        expect(screen.getByText('Junior Software Engineer')).toBeInTheDocument()
        expect(screen.queryByText('Frontend Developer')).not.toBeInTheDocument()
        expect(screen.queryByText('Backend Developer')).not.toBeInTheDocument()
    })

    // Employment type filter

    it('filters jobs by employment type', async () => {
        const user = userEvent.setup()
        await renderLoadedJobs()

        await user.selectOptions(screen.getByRole('combobox', { name: 'Employment type' }), 'Part-time')

        expect(screen.getByText('Frontend Developer')).toBeInTheDocument()
        expect(screen.queryByText('Junior Software Engineer')).not.toBeInTheDocument()
        expect(screen.queryByText('Backend Developer')).not.toBeInTheDocument()
    })

    // Text search

    it('searches jobs by title', async () => {
        const user = userEvent.setup()
        await renderLoadedJobs()

        await user.type(
            screen.getByPlaceholderText(
                'Search jobs by title, company or keyword...'
            ),
            'Frontend'
        )

        expect(screen.getByText('Frontend Developer')).toBeInTheDocument()
        expect(screen.queryByText('Junior Software Engineer')).not.toBeInTheDocument()
        expect(screen.queryByText('Backend Developer')).not.toBeInTheDocument()
    })

    it('searches jobs by company', async () => {
        const user = userEvent.setup()
        await renderLoadedJobs()

        await user.type(
            screen.getByPlaceholderText(
                'Search jobs by title, company or keyword...'
            ),
            'Google'
        )

        expect(screen.getByText('Junior Software Engineer')).toBeInTheDocument()
        expect(screen.getByText('Backend Developer')).toBeInTheDocument()
        expect(screen.queryByText('Frontend Developer')).not.toBeInTheDocument()
    })

    it('searches jobs by description keywords', async () => {
        const user = userEvent.setup()
        await renderLoadedJobs()

        await user.type(
            screen.getByPlaceholderText(
                'Search jobs by title, company or keyword...'
            ),
            'Python'
        )

        expect(screen.getByText('Junior Software Engineer')).toBeInTheDocument()
        expect(screen.queryByText('Frontend Developer')).not.toBeInTheDocument()
        expect(screen.queryByText('Backend Developer')).not.toBeInTheDocument()
    })

    it('performs case-insensitive searches', async () => {
        const user = userEvent.setup()
        await renderLoadedJobs()

        await user.type(
            screen.getByPlaceholderText(
                'Search jobs by title, company or keyword...'
            ),
            'python'
        )

        expect(screen.getByText('Junior Software Engineer')).toBeInTheDocument()
    })

    // Combined filters

    it('applies multiple filters simultaneously', async () => {
        const user = userEvent.setup()
        await renderLoadedJobs()

        await user.selectOptions(
            screen.getByRole('combobox', { name: 'Company' }),
            'Google'
        )

        await user.selectOptions(
            screen.getByRole('combobox', { name: 'Location' }),
            'Madrid'
        )

        expect(screen.getByText('Backend Developer')).toBeInTheDocument()
        expect(screen.queryByText('Junior Software Engineer')).not.toBeInTheDocument()
        expect(screen.queryByText('Frontend Developer')).not.toBeInTheDocument()
    })

    it('displays a message when no jobs match the filters', async () => {
        const user = userEvent.setup()
        await renderLoadedJobs()

        await user.selectOptions(screen.getByRole('combobox', { name: 'Company' }), 'Amazon')
        await user.selectOptions(screen.getByRole('combobox', { name: 'Location' }), 'Barcelona')

        expect(screen.getByText('No jobs match your filters')).toBeInTheDocument()
    })

    // Clear filters

    it('clears all filters and restores all jobs', async () => {
        const user = userEvent.setup()
        await renderLoadedJobs()

        await user.selectOptions(screen.getByRole('combobox', { name: 'Company' }), 'Amazon')
        await user.selectOptions(screen.getByRole('combobox', { name: 'Location' }), 'Madrid')

        await user.type(
            screen.getByPlaceholderText(
                'Search jobs by title, company or keyword...'
            ),
            'Frontend'
        )

        await user.click(screen.getByRole('button', { name: 'Clear filters' }))

        expect(screen.getByText('Junior Software Engineer')).toBeInTheDocument()
        expect(screen.getByText('Frontend Developer')).toBeInTheDocument()
        expect(screen.getByText('Backend Developer')).toBeInTheDocument()
    })
})
