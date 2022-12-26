package com.newsblur.fragment

import android.app.Dialog
import android.content.ClipData
import android.content.ClipboardManager
import android.os.Bundle
import androidx.appcompat.app.AlertDialog
import androidx.fragment.app.DialogFragment
import com.newsblur.R
import com.newsblur.databinding.NewsletterDialogBinding
import com.newsblur.util.PrefsUtils
import com.newsblur.util.setViewGone
import com.newsblur.util.setViewVisible

class NewslettersFragment : DialogFragment() {

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val view = layoutInflater.inflate(R.layout.newsletter_dialog, null)
        val binding: NewsletterDialogBinding = NewsletterDialogBinding.bind(view)
        val emailAddress = generateEmail()

        binding.txtEmail.text = emailAddress
        binding.btnSetup.setOnClickListener {
            binding.btnSetup.setViewGone()
            binding.txtSetup.setViewVisible()
        }

        return AlertDialog.Builder(requireContext()).apply {
            setView(binding.root)
            setPositiveButton(android.R.string.ok, null)
            setNegativeButton(R.string.copy_email) { _, _ ->
                copyToClipboard(emailAddress)
            }
        }.create()
    }

    private fun generateEmail(): String {
        val userDetails = PrefsUtils.getUserDetails(requireContext())
        return "${userDetails.username}-12345678@newsletters.newsblur.com"
    }

    private fun copyToClipboard(message: String) {
        val clipboardManager = requireContext().getSystemService(ClipboardManager::class.java)
        val clipData = ClipData.newPlainText("NewsBlur email forwarding", message)
        clipboardManager.setPrimaryClip(clipData)
    }
}