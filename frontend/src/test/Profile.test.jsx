
import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import userEvent from '@testing-library/user-event'
import Profile from '../components/Profile'

const mockProfile = {
    id: 1,
    target_role: 'Software Engineer',
    location: 'Barcelona',
    country: 'Spain',
    seniority: 'Graduate',
    work_arrangements: ['Remote', 'Hybrid'],
    preferred_skills: ['Python', 'React', 'Django']
}

describe('Profile', () => {
    beforeEach(() => {
        vi.stubGlobal(
            'fetch',
            vi.fn().mockReturnValue(new Promise(() => {}))
        )
    })

    const loadProfile = (profile = mockProfile) => {
        fetch
            .mockResolvedValueOnce({
                ok: true,
                json: async () => ({ id: profile.id })
            })
            .mockResolvedValueOnce({
                ok: true,
                json: async () => profile
            })
    }

    const renderLoadedProfile = async (profile = mockProfile) => {
        loadProfile(profile)
        render(<Profile />)

        await screen.findByDisplayValue('Software Engineer')
    }

    // Loading and API

    it('displays the loading message initially', () => {
        render(<Profile />)

        expect(screen.getByText('Loading...')).toBeInTheDocument()
    })

    it('fetches the active profile and then its details', async () => {
        await renderLoadedProfile()

        expect(fetch).toHaveBeenNthCalledWith(
            1,
            'http://127.0.0.1:8000/jobs/profiles/active/'
        )

        expect(fetch).toHaveBeenNthCalledWith(
            2,
            'http://127.0.0.1:8000/jobs/profiles/1/'
        )
    })

    it('displays an error if loading the profile fails', async () => {
        fetch.mockRejectedValueOnce(new Error('Network error'))

        render(<Profile />)

        expect(await screen.findByText('Network error')).toBeInTheDocument()
    })

    it('displays an error if the response is unsuccessful', async () => {
        fetch.mockResolvedValueOnce({ ok: false })

        render(<Profile />)

        expect(await screen.findByText('Could not find an active profile')).toBeInTheDocument()    })

    // Profile rendering

    it('displays the profile information', async () => {
        await renderLoadedProfile()

        expect(screen.getByDisplayValue('Software Engineer')).toBeInTheDocument()
        expect(screen.getByDisplayValue('Barcelona')).toBeInTheDocument()
        expect(screen.getByDisplayValue('Spain')).toBeInTheDocument()
    })

    it('displays the correct seniority', async () => {
        await renderLoadedProfile()

        expect(screen.getByRole('combobox')).toHaveValue('Graduate')
    })

    it('displays the selected work arrangements', async () => {
        await renderLoadedProfile()

        expect(screen.getByRole('checkbox', { name: 'Remote' })).toBeChecked()
        expect(screen.getByRole('checkbox', { name: 'Hybrid' })).toBeChecked()
        expect(screen.getByRole('checkbox', { name: 'On-site' })).not.toBeChecked()
    })

    it('displays the preferred skills', async () => {
        await renderLoadedProfile()

        expect(
            screen.getByDisplayValue('Python, React, Django')
        ).toBeInTheDocument()
    })

    // Editing profile information

    it('allows the user to edit the target role', async () => {
        const user = userEvent.setup()
        await renderLoadedProfile()

        const input = screen.getByDisplayValue('Software Engineer')

        await user.clear(input)
        await user.type(input, 'Backend Developer')

        expect(input).toHaveValue('Backend Developer')
    })

    it('allows the user to edit the location', async () => {
        const user = userEvent.setup()
        await renderLoadedProfile()

        const input = screen.getByDisplayValue('Barcelona')

        await user.clear(input)
        await user.type(input, 'Madrid')

        expect(input).toHaveValue('Madrid')
    })

    it('allows the user to change seniority', async () => {
        const user = userEvent.setup()
        await renderLoadedProfile()

        await user.selectOptions(
            screen.getByRole('combobox'),
            'Junior'
        )

        expect(screen.getByRole('combobox')).toHaveValue('Junior')
    })

    it('allows the user to change work arrangements', async () => {
        const user = userEvent.setup()
        await renderLoadedProfile()

        await user.click(screen.getByRole('checkbox', { name: 'Remote' }))
        await user.click(screen.getByRole('checkbox', { name: 'On-site' }))

        expect(screen.getByRole('checkbox', { name: 'Remote' })).not.toBeChecked()
        expect(screen.getByRole('checkbox', { name: 'On-site' })).toBeChecked()
    })

    it('allows the user to edit preferred skills', async () => {
        const user = userEvent.setup()
        await renderLoadedProfile()

        const input = screen.getByDisplayValue('Python, React, Django')

        await user.clear(input)
        await user.type(input, 'Java, Spring, PostgreSQL')

        expect(input).toHaveValue('Java, Spring, PostgreSQL')
    })

    // Saving profile

    it('sends an update request when saving changes', async () => {
        const user = userEvent.setup()
        await renderLoadedProfile()

        fetch.mockResolvedValueOnce({
            ok: true,
            text: async () => JSON.stringify(mockProfile)
        })

        await user.click(screen.getByRole('button', { name: 'Save changes' }))

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                'http://127.0.0.1:8000/jobs/profiles/1/update/',
                expect.objectContaining({
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
            )
        })
    })

    it('sends the updated profile information in the request body', async () => {
        const user = userEvent.setup()
        await renderLoadedProfile()

        fetch.mockResolvedValueOnce({
            ok: true,
            text: async () => JSON.stringify(mockProfile)
        })

        const input = screen.getByDisplayValue('Python, React, Django')

        await user.clear(input)
        await user.type(input, 'Java, Spring')

        await user.click(screen.getByRole('button', { name: 'Save changes' }))

        await waitFor(() => {
            const saveCall = fetch.mock.calls.find(
                call => call[1]?.method === 'PUT'
            )

            expect(saveCall).toBeDefined()

            const body = JSON.parse(saveCall[1].body)

            expect(body.preferred_skills).toEqual(['Java', 'Spring'])
        })
    })

    it('displays a success message after saving', async () => {
        const user = userEvent.setup()
        await renderLoadedProfile()

        fetch.mockResolvedValueOnce({
            ok: true,
            text: async () => JSON.stringify(mockProfile)
        })

        await user.click(screen.getByRole('button', { name: 'Save changes' }))

        expect(
            await screen.findByText('Profile saved successfully!')
        ).toBeInTheDocument()
    })

    it('displays an error if saving fails', async () => {
        const user = userEvent.setup()
        await renderLoadedProfile()

        fetch.mockResolvedValueOnce({
            ok: false,
            status: 400,
            text: async () => 'Invalid profile data'
        })

        await user.click(screen.getByRole('button', { name: 'Save changes' }))

        expect(
            await screen.findByText('Error 400: Invalid profile data')
        ).toBeInTheDocument()
    })

    // Handling missing profile data

    it('handles missing preferred skills', async () => {
        const profile = {
            ...mockProfile,
            preferred_skills: null
        }

        loadProfile(profile)
        render(<Profile />)

        expect(
            await screen.findByPlaceholderText(
                'e.g. Python, React, Django, SQL'
            )
        ).toHaveValue('')
    })

    it('handles missing work arrangements', async () => {
        const profile = {
            ...mockProfile,
            work_arrangements: null
        }

        loadProfile(profile)
        render(<Profile />)

        expect(
            await screen.findByRole('checkbox', { name: 'Remote' })
        ).not.toBeChecked()
    })
})
