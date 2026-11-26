import { render, screen, within } from '@testing-library/react'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import Dashboard from '../components/Dashboard'

const mockJobs = [
    {
        id: 1,
        title: 'Alpha Developer',
        company: 'Company A',
        location: 'Barcelona',
        job_type: 'Full-time',
        relevance_score: 80,
        date_posted: '2026-01-01',
        posting_link: 'https://example.com/1'
    },
    {
        id: 2,
        title: 'Beta Developer',
        company: 'Company B',
        location: 'Barcelona',
        job_type: 'Full-time',
        relevance_score: 95,
        date_posted: '2026-01-02',
        posting_link: 'https://example.com/2'
    },
    {
        id: 3,
        title: 'Gamma Developer',
        company: 'Company C',
        location: 'Barcelona',
        job_type: 'Full-time',
        relevance_score: 70,
        date_posted: '2026-01-03',
        posting_link: 'https://example.com/3'
    },
    {
        id: 4,
        title: 'Delta Developer',
        company: 'Company D',
        location: 'Barcelona',
        job_type: 'Full-time',
        relevance_score: 88,
        date_posted: '2026-01-04',
        posting_link: 'https://example.com/4'
    },
    {
        id: 5,
        title: 'Epsilon Developer',
        company: 'Company E',
        location: 'Barcelona',
        job_type: 'Full-time',
        relevance_score: 60,
        date_posted: '2026-01-05',
        posting_link: 'https://example.com/5'
    },
    {
        id: 6,
        title: 'Zeta Developer',
        company: 'Company F',
        location: 'Barcelona',
        job_type: 'Full-time',
        relevance_score: 99,
        date_posted: '2026-01-06',
        posting_link: 'https://example.com/6'
    },
    {
        id: 7,
        title: 'Eta Developer',
        company: 'Company G',
        location: 'Barcelona',
        job_type: 'Full-time',
        relevance_score: null,
        date_posted: '2026-01-07',
        posting_link: 'https://example.com/7'
    },
    {
        id: 8,
        title: 'Theta Developer',
        company: 'Company H',
        location: 'Barcelona',
        job_type: 'Full-time',
        relevance_score: 50,
        date_posted: null,
        posting_link: 'https://example.com/8'
    }
]

describe('Dashboard', () => {

    const getSection = async (heading) => {
        const headingElement = await screen.findByRole('heading', {
            name: heading
        })

        return headingElement.closest('section')
    }

    beforeEach(() => {
        vi.stubGlobal('fetch', vi.fn())
    })

    it('displays the loading message initially', () => {
        fetch.mockReturnValue(new Promise(() => {}))

        render(<Dashboard />)

        expect(screen.getByText('Loading jobs...')).toBeInTheDocument()
    })

    it('fetches jobs from the correct API endpoint', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => []
        })

        render(<Dashboard />)

        expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/jobs/')
        expect(await screen.findByText('No jobs found')).toBeInTheDocument()
    })

    it('displays an error when the request fails', async () => {
        fetch.mockRejectedValue(new Error('Network error'))

        render(<Dashboard />)

        expect(
            await screen.findByText('Unable to load jobs. Please try again later.')
        ).toBeInTheDocument()
    })

    it('displays an error when the API response is unsuccessful', async () => {
        fetch.mockResolvedValue({
            ok: false
        })

        render(<Dashboard />)

        expect(
            await screen.findByText('Unable to load jobs. Please try again later.')
        ).toBeInTheDocument()
    })

    it('displays No jobs found when the API returns an empty list', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => []
        })

        render(<Dashboard />)

        expect(await screen.findByText('No jobs found')).toBeInTheDocument()
    })

    it('displays the total number of jobs', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockJobs
        })

        render(<Dashboard />)

        expect(await screen.findByText('8', { exact: true })).toBeInTheDocument()
    })

    it('calculates the average match score correctly', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockJobs
        })

        render(<Dashboard />)

        expect(await screen.findByText('77.4', { exact: true })).toBeInTheDocument()
    })

    it('displays the highest match score', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockJobs
        })

        render(<Dashboard />)

        expect(await screen.findByText('99', { exact: true })).toBeInTheDocument()
    })

    it('displays N/A for average and highest scores when no jobs have a score', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => [
                { ...mockJobs[0], relevance_score: null },
                { ...mockJobs[1], relevance_score: null }
            ]
        })

        render(<Dashboard />)

        const results = await screen.findAllByText('N/A')

        expect(results).toHaveLength(2)
    })

    it('displays recommended jobs ordered by match score', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockJobs
        })

        render(<Dashboard />)

        const section = await getSection('Recommended Jobs')

        const titles = within(section)
            .getAllByRole('link')
            .map(link => link.textContent)

        expect(titles).toEqual([
            'Zeta Developer',
            'Beta Developer',
            'Delta Developer',
            'Alpha Developer',
            'Gamma Developer'
        ])
    })

    it('displays no more than five recommended jobs', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockJobs
        })

        render(<Dashboard />)

        const section = await getSection('Recommended Jobs')

        expect(await within(section).findAllByRole('link')).toHaveLength(5)
    })

    it('displays recent jobs ordered by posting date', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockJobs
        })

        render(<Dashboard />)

        const section = await getSection('Recently Posted')

        const titles = within(section)
            .getAllByRole('link')
            .map(link => link.textContent)

        expect(titles).toEqual([
            'Eta Developer',
            'Zeta Developer',
            'Epsilon Developer',
            'Delta Developer',
            'Gamma Developer'
        ])
    })

    it('displays no more than five recently posted jobs', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockJobs
        })

        render(<Dashboard />)

        const section = await getSection('Recently Posted')

        expect(await within(section).findAllByRole('link')).toHaveLength(5)
    })

    it('excludes jobs without a match score from recommended jobs', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockJobs
        })

        render(<Dashboard />)

        const section = await getSection('Recommended Jobs')

        expect(
            within(section).queryByRole('link', { name: 'Eta Developer' })
        ).not.toBeInTheDocument()
    })

    it('excludes jobs without a posting date from recently posted jobs', async () => {
        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockJobs
        })

        render(<Dashboard />)

        const section = await getSection('Recently Posted')

        expect(
            within(section).queryByRole('link', { name: 'Theta Developer' })
        ).not.toBeInTheDocument()
    })

})